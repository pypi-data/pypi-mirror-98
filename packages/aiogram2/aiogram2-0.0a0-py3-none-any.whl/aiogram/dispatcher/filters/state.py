import inspect
from typing import Optional

from ..dispatcher import Dispatcher, FSMContext


class State:
    """
    State object
    """

    def __init__(self, state: Optional[str] = None, group_name: Optional[str] = None):
        self._state = state
        self._group_name = group_name
        self._group = None

    @property
    def group(self):
        if not self._group:
            raise RuntimeError('This state is not in any group.')
        return self._group

    def get_root(self):
        return self.group.get_root()

    @property
    def state(self):
        if self._state is None or self._state == '*':
            return self._state

        if self._group_name is None and self._group:
            group = self._group.__full_group_name__
        elif self._group_name:
            group = self._group_name
        else:
            group = '@'

        return f'{group}:{self._state}'

    def set_parent(self, group):
        if not issubclass(group, StatesGroup):
            raise ValueError('Group must be subclass of StatesGroup')
        self._group = group

    def __set_name__(self, owner, name):
        if self._state is None:
            self._state = name
        self.set_parent(owner)

    def __str__(self):
        return f"<State '{self.state or ''}'>"

    __repr__ = __str__

    async def set(self):
        state = Dispatcher.get_current().current_state()
        await state.set_state(self.state)


class StatesGroupMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super(StatesGroupMeta, mcs).__new__(mcs, name, bases, namespace)

        states = []
        childs = []

        cls._group_name = name

        for name, prop in namespace.items():

            if isinstance(prop, State):
                states.append(prop)
                StatesGroup.all_states_groups_states.add(prop)
            elif inspect.isclass(prop) and issubclass(prop, StatesGroup):
                childs.append(prop)
                prop._parent = cls

        cls._parent = None
        cls._childs = tuple(childs)
        cls._states = tuple(states)
        cls._state_names = tuple(state.state for state in states)

        return cls

    @property
    def state_ctx(cls) -> FSMContext:
        return Dispatcher.get_current().current_state()

    @property
    def __group_name__(cls) -> str:
        return cls._group_name

    @property
    def __full_group_name__(cls) -> str:
        if cls._parent:
            return '.'.join((cls._parent.__full_group_name__, cls._group_name))
        return cls._group_name

    @property
    def states(cls) -> tuple:
        return cls._states

    @property
    def childs(cls) -> tuple:
        return cls._childs

    @property
    def all_childs(cls):
        result = cls.childs
        for child in cls.childs:
            result += child.childs
        return result

    @property
    def all_states(cls):
        result = cls.states
        for group in cls.childs:
            result += group.all_states
        return result

    @property
    def all_states_names(cls):
        return tuple(state.state for state in cls.all_states)

    @property
    def states_names(cls) -> tuple:
        return tuple(state.state for state in cls.states)

    def get_root(cls):
        if cls._parent is None:
            return cls
        return cls._parent.get_root()

    def __contains__(cls, item):
        if isinstance(item, str):
            return item in cls.all_states_names
        if isinstance(item, State):
            return item in cls.all_states
        if isinstance(item, StatesGroup):
            return item in cls.all_childs
        return False

    def __str__(self):
        return f"<StatesGroup '{self.__full_group_name__}'>"


class StatesGroup(metaclass=StatesGroupMeta):
    all_states_groups_states = set()

    @classmethod
    def get_state_by_name(cls, state_name: str) -> Optional[State]:
        """Search for State with state_name in all StatesGroups."""
        for state in cls.all_states_groups_states:
            if state.state == state_name:
                return state

    @staticmethod
    def get_state_by_index(group_states: tuple[State], index: int) -> Optional[State]:
        """Return state with passed index from group or None. Exception safety."""
        if 0 <= index < len(group_states):
            return group_states[index]

    @classmethod
    async def get_current_state(cls) -> Optional[State]:
        """Search current State instance in all StatesGroups."""
        try:
            state_name = await cls.state_ctx.get_state()
            return cls.get_state_by_name(state_name)
        except AttributeError:
            return None

    @classmethod
    async def get_next_state(cls) -> Optional[State]:
        state = await cls.get_current_state()

        try:
            group_states: tuple[State] = state.group.states
        except AttributeError:
            return None

        next_step = group_states.index(state) + 1
        return cls.get_state_by_index(group_states, next_step)

    @classmethod
    async def get_previous_state(cls) -> Optional[State]:
        state = await cls.get_current_state()

        try:
            group_states: tuple[State] = state.group.states
        except AttributeError:
            return None

        previous_step = group_states.index(state) - 1
        return cls.get_state_by_index(group_states, previous_step)

    @classmethod
    async def get_first_group_state(cls) -> Optional[State]:
        state = await cls.get_current_state()

        try:
            group_states: tuple[State] = state.group.states
            return group_states[0]
        except AttributeError:
            return None

    @classmethod
    async def get_last_group_state(cls) -> Optional[State]:
        state = await cls.get_current_state()

        try:
            group_states: tuple[State] = state.group.states
            return group_states[-1]
        except AttributeError:
            return None

    @classmethod
    async def next(cls) -> str:
        state = Dispatcher.get_current().current_state()
        state_name = await state.get_state()

        try:
            next_step = cls.states_names.index(state_name) + 1
        except ValueError:
            next_step = 0

        try:
            next_state_name = cls.states[next_step].state
        except IndexError:
            next_state_name = None

        await state.set_state(next_state_name)
        return next_state_name

    @classmethod
    async def previous(cls) -> str:
        state = Dispatcher.get_current().current_state()
        state_name = await state.get_state()

        try:
            previous_step = cls.states_names.index(state_name) - 1
        except ValueError:
            previous_step = 0

        if previous_step < 0:
            previous_state_name = None
        else:
            previous_state_name = cls.states[previous_step].state

        await state.set_state(previous_state_name)
        return previous_state_name

    @classmethod
    async def first(cls) -> str:
        state = Dispatcher.get_current().current_state()
        first_step_name = cls.states_names[0]

        await state.set_state(first_step_name)
        return first_step_name

    @classmethod
    async def last(cls) -> str:
        state = Dispatcher.get_current().current_state()
        last_step_name = cls.states_names[-1]

        await state.set_state(last_step_name)
        return last_step_name


default_state = State()
any_state = State(state='*')
