from dataclasses import dataclass, field
from typing import Callable, List, Optional

from .api.command.v1 import Command, ScheduleActivityTaskCommandAttributes, StartTimerCommandAttributes, \
    CancelTimerCommandAttributes, RequestCancelActivityTaskCommandAttributes
from .api.enums.v1 import CommandType
from .api.history.v1 import HistoryEvent

from .decisions import DecisionState, DecisionId
from .exceptions import IllegalStateException, IllegalArgumentException


class DecisionStateMachine:
    def get_decision(self) -> Optional[Command]:
        raise NotImplementedError

    def cancel(self, immediate_cancellation_callback: Callable) -> bool:
        raise NotImplementedError

    def handle_started_event(self, event: HistoryEvent):
        raise NotImplementedError

    def handle_cancellation_initiated_event(self):
        raise NotImplementedError

    def handle_cancellation_event(self):
        raise NotImplementedError

    def handle_cancellation_failure_event(self, event: HistoryEvent):
        raise NotImplementedError

    def handle_completion_event(self):
        raise NotImplementedError

    def handle_initiation_failed_event(self, event: HistoryEvent):
        raise NotImplementedError

    def handle_initiated_event(self, event: HistoryEvent):
        raise NotImplementedError

    def handle_decision_task_started_event(self):
        raise NotImplementedError

    def get_state(self) -> DecisionState:
        raise NotImplementedError

    def is_done(self) -> bool:
        raise NotImplementedError

    def get_id(self) -> DecisionId:
        raise NotImplementedError


# noinspection PyAbstractClass
@dataclass
class DecisionStateMachineBase(DecisionStateMachine):
    """
    This class has feature parity with the Java version even though it implements parts of features
    not yet implemented in the Python version.
    """
    id: DecisionId = None
    state: DecisionState = DecisionState.CREATED
    state_history: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.state_history.append(str(self))

    def get_state(self) -> DecisionState:
        return self.state

    def get_id(self) -> DecisionId:
        return self.id

    def is_done(self) -> bool:
        return self.state in (DecisionState.COMPLETED,
                              DecisionState.COMPLETED_AFTER_CANCELLATION_DECISION_SENT)

    def handle_decision_task_started_event(self):
        if self.state == DecisionState.CREATED:
            self.state_history.append("handle_decision_task_started_event")
            self.state = DecisionState.DECISION_SENT
            self.state_history.append(str(self.state))
        else:
            pass

    def cancel(self, immediate_cancellation_callback: Optional[Callable]) -> bool:
        self.state_history.append("cancel")
        result = False
        if self.state == DecisionState.CREATED:
            self.state = DecisionState.COMPLETED
            if immediate_cancellation_callback:
                immediate_cancellation_callback()
        elif self.state == DecisionState.DECISION_SENT:
            self.state = DecisionState.CANCELED_BEFORE_INITIATED
            result = True
        elif self.state == DecisionState.INITIATED:
            self.state = DecisionState.CANCELED_AFTER_INITIATED
            result = True
        else:
            self.fail_state_transition()
        self.state_history.append(str(self.state))
        return result

    def handle_initiated_event(self, event: HistoryEvent):
        self.state_history.append("handle_initiated_event")
        if self.state == DecisionState.DECISION_SENT:
            self.state = DecisionState.INITIATED
        elif self.state == DecisionState.CANCELED_BEFORE_INITIATED:
            self.state = DecisionState.CANCELED_AFTER_INITIATED
        else:
            self.fail_state_transition()
        self.state_history.append(str(self.state))

    def handle_initiation_failed_event(self, event: HistoryEvent):
        self.state_history.append("handle_initiation_failed_event")
        if self.state in (
                DecisionState.INITIATED, DecisionState.DECISION_SENT, DecisionState.CANCELED_BEFORE_INITIATED):
            self.state = DecisionState.COMPLETED
        else:
            self.fail_state_transition()
        self.state_history.append(str(self.state))

    def handle_started_event(self, event: HistoryEvent):
        self.state_history.append("handle_started_event")

    def handle_completion_event(self):
        self.state_history.append("handle_completion_event")
        if self.state in (DecisionState.CANCELED_AFTER_INITIATED, DecisionState.INITIATED):
            self.state = DecisionState.COMPLETED
        elif self.state == DecisionState.CANCELLATION_DECISION_SENT:
            self.state = DecisionState.COMPLETED_AFTER_CANCELLATION_DECISION_SENT
        else:
            self.fail_state_transition()
        self.state_history.append(str(self.state))

    def handle_cancellation_initiated_event(self):
        self.state_history.append("handle_cancellation_initiated_event")
        if self.state == DecisionState.CANCELLATION_DECISION_SENT:
            # No state change
            pass
        else:
            self.fail_state_transition()
        self.state_history.append(str(self.state))

    def handle_cancellation_failure_event(self, event: HistoryEvent):
        self.state_history.append("handle_cancellation_failure_event")
        if self.state == DecisionState.COMPLETED_AFTER_CANCELLATION_DECISION_SENT:
            self.state = DecisionState.COMPLETED
        else:
            self.fail_state_transition()
        self.state_history.append(str(self.state))

    def handle_cancellation_event(self):
        self.state_history.append("handle_cancellation_event")
        if self.state == DecisionState.CANCELLATION_DECISION_SENT:
            self.state = DecisionState.COMPLETED
        else:
            self.fail_state_transition()
        self.state_history.append(str(self.state))

    def fail_state_transition(self):
        raise IllegalStateException("id=" + str(self.id) + ", transitions=" + str(self.state_history))


@dataclass
class ActivityDecisionStateMachine(DecisionStateMachineBase):
    """
    This class has feature parity with the Java version even though it implements parts of features
    not yet implemented in the Python version.
    """
    schedule_attributes: ScheduleActivityTaskCommandAttributes = None

    def __post_init__(self):
        if not self.schedule_attributes:
            raise IllegalArgumentException("schedule_attributes is mandatory")

    def get_decision(self) -> Optional[Command]:
        if self.state == DecisionState.CREATED:
            return self.create_schedule_activity_task_decision()
        elif self.state == DecisionState.CANCELED_AFTER_INITIATED:
            return self.create_request_cancel_activity_task_decision()
        else:
            return None

    def handle_decision_task_started_event(self):
        if self.state == DecisionState.CANCELED_AFTER_INITIATED:
            self.state_history.append("handle_decision_task_started_event")
            self.state = DecisionState.CANCELLATION_DECISION_SENT
            self.state_history.append(str(self.state))
        else:
            super().handle_decision_task_started_event()

    def handle_cancellation_failure_event(self, event: HistoryEvent):
        if self.state == DecisionState.CANCELLATION_DECISION_SENT:
            self.state_history.append("handle_cancellation_failure_event")
            self.state = DecisionState.INITIATED
            self.state_history.append(str(self.state))
        else:
            super().handle_cancellation_failure_event(event)

    def create_schedule_activity_task_decision(self) -> Command:
        decision: Command = Command()
        decision.schedule_activity_task_command_attributes = self.schedule_attributes
        decision.command_type = CommandType.COMMAND_TYPE_SCHEDULE_ACTIVITY_TASK
        return decision

    def create_request_cancel_activity_task_decision(self) -> Command:
        try_cancel = RequestCancelActivityTaskCommandAttributes()
        try_cancel.activity_id = self.schedule_attributes.activity_id
        decision: Command = Command()
        decision.request_cancel_activity_task_command_attributes = try_cancel
        decision.command_type = CommandType.COMMAND_TYPE_REQUEST_CANCEL_ACTIVITY_TASK
        return decision


# noinspection PyAbstractClass
@dataclass
class CompleteWorkflowStateMachine(DecisionStateMachine):
    id: DecisionId
    decision: Optional[Command]

    def get_id(self) -> DecisionId:
        return self.id

    def get_decision(self) -> Optional[Command]:
        return self.decision

    def handle_initiation_failed_event(self, event: HistoryEvent):
        self.decision = None

    def get_state(self) -> DecisionState:
        return DecisionState.CREATED

    def is_done(self) -> bool:
        return self.decision is not None

    def handle_decision_task_started_event(self):
        pass


# noinspection PyAbstractClass
@dataclass
class TimerDecisionStateMachine(DecisionStateMachineBase):
    start_timer_attributes: StartTimerCommandAttributes = None
    canceled: bool = False

    def __post_init__(self):
        if not self.start_timer_attributes:
            raise IllegalArgumentException("start_timer_decision_attributes is mandatory")

    def get_decision(self) -> Optional[Command]:
        if self.state == DecisionState.CREATED:
            return self.create_start_timer_decision()
        elif self.state == DecisionState.CANCELED_AFTER_INITIATED:
            return self.create_cancel_timer_decision()
        else:
            return None

    def handle_decision_task_started_event(self):
        if self.state == DecisionState.CANCELED_AFTER_INITIATED:
            self.state_history.append("handle_decision_task_started_event")
            self.state = DecisionState.CANCELLATION_DECISION_SENT
            self.state_history.append(str(self.state))
        else:
            super().handle_decision_task_started_event()

    def handle_cancellation_failure_event(self, event: HistoryEvent):
        if self.state == DecisionState.CANCELLATION_DECISION_SENT:
            self.state_history.append("handle_cancellation_failure_event")
            self.state = DecisionState.INITIATED
            self.state_history.append(str(self.state))
        else:
            super().handle_cancellation_failure_event(event)

    def cancel(self, immediate_cancellation_callback: Optional[Callable]) -> bool:
        self.canceled = True
        immediate_cancellation_callback()
        return super().cancel(None)

    def is_done(self) -> bool:
        return self.state == DecisionState.COMPLETED or self.canceled

    def create_cancel_timer_decision(self) -> Command:
        try_cancel = CancelTimerCommandAttributes()
        try_cancel.timer_id = self.start_timer_attributes.timer_id
        decision: Command = Command()
        decision.cancel_timer_command_attributes = try_cancel
        decision.command_type = CommandType.COMMAND_TYPE_CANCEL_TIMER
        return decision

    def create_start_timer_decision(self) -> Command:
        decision: Command = Command()
        decision.start_timer_command_attributes = self.start_timer_attributes
        decision.command_type = CommandType.COMMAND_TYPE_START_TIMER
        return decision


@dataclass
class MarkerDecisionStateMachine(DecisionStateMachineBase):
    decision: Command = None

    def get_decision(self) -> Optional[Command]:
        if self.state == DecisionState.CREATED:
            return self.decision
        else:
            return None



