"""List and filtered list model."""

# standard libraries
import copy
import functools
import operator
import threading
import typing

# third party libraries
# None

# local libraries
from nion.utils import Event
from nion.utils import Observable
from nion.utils import Selection

T = typing.TypeVar('T')


class ListModel(Observable.Observable, typing.Generic[T]):

    def __init__(self, key: str = None, items: typing.Sequence[T] = None):
        super().__init__()
        self.__key = key
        self.__items : typing.List[T] = list(items) if items else list()

    def close(self) -> None:
        pass

    def clear_items(self) -> None:
        while self.__items:
            self.remove_item(len(self.__items) - 1)

    def insert_item(self, index: int, value: T) -> None:
        self.__items.insert(index, value)
        self.notify_insert_item(self.__key if self.__key else "items", value, index)

    def remove_item(self, index: int) -> None:
        value = self.__items[index]
        del self.__items[index]
        self.notify_remove_item(self.__key if self.__key else "items", value, index)

    def append_item(self, value: T) -> None:
        self.insert_item(len(self.__items), value)

    @property
    def items(self) -> typing.List[T]:
        return self.__items

    @items.setter
    def items(self, items: typing.List[T]) -> None:
        self.clear_items()
        for item in items:
            self.insert_item(len(self.__items), item)

    def __getattr__(self, item: str) -> typing.List[T]:
        if self.__key and item == self.__key:
            return self.items
        raise AttributeError()


class Filter:
    def __init__(self, default: bool=False):
        self.__default = default

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__default = self.__default
        return result

    def matches(self, d) -> bool:
        return self.__default


class AndFilter(Filter):
    def __init__(self, filters: typing.Sequence[Filter]=None):
        super().__init__()
        self.__filters = copy.copy(filters) if filters else list()

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.__filters = copy.deepcopy(self.__filters, memo)
        return result

    def matches(self, d) -> bool:
        return all(map(operator.methodcaller('matches', d), self.__filters))


class OrFilter(Filter):
    def __init__(self, filters: typing.Sequence[Filter]=None):
        super().__init__()
        self.__filters = copy.copy(filters) if filters else list()

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.__filters = copy.deepcopy(self.__filters, memo)
        return result

    def matches(self, d) -> bool:
        return any(map(operator.methodcaller('matches', d), self.__filters))


class NotFilter(Filter):
    def __init__(self, filter: Filter):
        super().__init__()
        self.__filter = filter

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.__filter = copy.deepcopy(self.__filter, memo)
        return result

    def matches(self, d) -> bool:
        return not self.__filter.matches(d)


class EqFilter(Filter):
    def __init__(self, key: str, value, cmp=None):
        super().__init__()
        self.__key = key
        self.__value = value
        self.__cmp = cmp if cmp else operator.eq

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.__key = self.__key
        result.__value = self.__value
        result.__cmp = self.__cmp
        return result

    def matches(self, d) -> bool:
        d_value = getattr(d, self.__key)
        return self.__cmp(d_value, self.__value)


class NotEqFilter(Filter):
    def __init__(self, key: str, value, cmp=None):
        super().__init__()
        self.__key = key
        self.__value = value
        self.__cmp = cmp if cmp else operator.eq

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.__key = self.__key
        result.__value = self.__value
        result.__cmp = self.__cmp
        return result

    def matches(self, d) -> bool:
        d_value = getattr(d, self.__key)
        return not self.__cmp(d_value, self.__value)


class StartsWithFilter(Filter):
    def __init__(self, key: str, value: str):
        super().__init__()
        self.__key = key
        self.__value = value

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.__key = self.__key
        result.__value = self.__value
        return result

    def matches(self, d) -> bool:
        d_value = getattr(d, self.__key)
        return d_value.startswith(self.__value)


class TextFilter(Filter):
    def __init__(self, key: str, text: str):
        super().__init__()
        self.__key = key
        self.__text = text
        self.__lower_text = text.lower()

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.__key = self.__key
        result.__text = self.__text
        return result

    def matches(self, d) -> bool:
        d_value = str(getattr(d, self.__key)).lower()
        return d_value.find(self.__lower_text) >= 0


class PartialDateFilter(Filter):
    def __init__(self, key: str, year: int=None, month: int=None, day: int=None):
        super().__init__()
        self.__key = key
        self.__year = year
        self.__month = month
        self.__day = day

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.__key = self.__key
        result.__year = self.__year
        result.__month = self.__month
        result.__day = self.__day
        return result

    def matches(self, d) -> bool:
        d_value = getattr(d, self.__key)
        if self.__year and d_value.year != self.__year:
            return False
        if self.__month and d_value.month != self.__month:
            return False
        if self.__day and d_value.day != self.__day:
            return False
        return True


class PredicateFilter(Filter):
    # used for testing, not serializable
    def __init__(self, predicate):
        super().__init__()
        self.__predicate = predicate

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result.__predicate = self.__predicate
        return result

    def matches(self, d) -> bool:
        return self.__predicate(d)


SortKeyCallable = typing.Optional[typing.Callable]


class FilteredListModel(Observable.Observable):
    """Filtered list of items.

    This class implements a filter function and a sorting function. Both the filter and
    sorting can be changed on the fly and this class will generate the appropriate insert
    and remove messages.

    Since changes can be slow, multiple changes are allowed to be made simultaneously by
    calling begin_change and end_change around the changes, or by using a context manager
    available via the changes method.
    """
    def __init__(self, *, container=None, master_items_key=None, items_key=None, selection=None):
        super().__init__()
        self.__container = None
        self.__master_items_key = master_items_key or items_key
        self.__items_key = items_key
        self.__master_items = list()  # a list of source items (to be filtered)
        self.__items = list()  # a list of filtered items
        self.__items_sorted = False
        self._update_mutex = threading.RLock()
        self.__filter = Filter(True)
        self.__sort_key: SortKeyCallable = None
        self.__sort_reverse = False
        self.__change_level = 0
        self.reset_list_event = Event.Event()
        self.begin_changes_event = Event.Event()
        self.end_changes_event = Event.Event()
        self.__item_changed_event_listeners = list()
        self.__item_inserted_event_listener = None
        self.__item_removed_event_listener = None
        self.__reset_list_event_listener = None
        self.__begin_changes_event_listener = None
        self.__end_changes_event_listener = None
        self.__selection_changes: typing.List[typing.Tuple[bool, int]] = list()
        self.__selections = list()
        if selection:
            self.__selections.append(selection)
        self.container = container

    def close(self):
        self.container = None
        self.__item_changed_event_listeners = None

    def begin_change(self):
        """ Begin a set of changes. Balance with end_changes. """
        self.__change_level += 1

    def end_change(self):
        """ End a set of changes and update items if finished. """
        with self._update_mutex:
            self.__change_level -= 1
            if self.__change_level == 0:
                self.__update_items()

    def changes(self):
        """ Acquire this while setting filter or sort so that changes get made simultaneously. """

        class ChangeTracker:
            def __init__(self, list_model: FilteredListModel):
                self.list_model = list_model

            def __enter__(self):
                self.list_model.begin_change()
                return self

            def __exit__(self, type_, value, traceback):
                self.list_model.end_change()

        return ChangeTracker(self)

    def mark_changed(self) -> None:
        with self.changes(): pass

    # thread safe.
    @property
    def sort_key(self) -> SortKeyCallable:
        """ Return the sort key function (for item). """
        return self.__sort_key

    @sort_key.setter
    def sort_key(self, value: SortKeyCallable) -> None:
        """ Set the sort key function. """
        with self._update_mutex:
            self.__sort_key = value
            self.__items_sorted = False
            self.reset_list_event.fire(self.__items_key)
        self.__update_items()

    @property
    def sort_reverse(self) -> bool:
        """ Return the sort reverse value. """
        return self.__sort_reverse

    @sort_reverse.setter
    def sort_reverse(self, value: bool) -> None:
        """ Set the sort reverse value. """
        with self._update_mutex:
            self.__sort_reverse = value
            self.__items_sorted = False
            self.reset_list_event.fire(self.__items_key)
        self.__update_items()

    # thread safe.
    @property
    def filter(self) -> Filter:
        """ Return the filter function. """
        return self.__filter

    @filter.setter
    def filter(self, value: Filter) -> None:
        """ Set the filter function. """
        self.__filter = value
        self.__items_sorted = False
        self.reset_list_event.fire(self.__items_key)
        self.__update_items()

    @property
    def items(self) -> typing.Sequence:
        """ Return the items. """
        with self._update_mutex:
            return copy.copy(self.__items)

    def __getattr__(self, item):
        if item == self.__items_key:
            return self.items
        raise AttributeError()

    # thread safe
    def _get_master_items(self):
        with self._update_mutex:
            return copy.copy(self.__master_items)

    def __find_sorted_index_for_item(self, item, items, sort_key, sort_operator):
        item_sort_key = sort_key(item)
        low = 0
        high = len(items)
        while low < high:
            mid = (low + high) // 2
            if sort_operator(sort_key(items[mid]), item_sort_key):
                low = mid + 1
            else:
                high = mid
        return low

    def __find_unsorted_index_for_item(self, item, master_items, filter):
        index = 0
        for item_ in master_items:
            if item_ == item:
                break
            if filter.matches(item_):
                index += 1
        return index

    # thread safe
    def __inserted_master_item(self, before_index, item):
        """
            Subclasses can call this to notify this object that a item in
            the master item list has been inserted.
        """
        with self._update_mutex:
            if self.__change_level > 0:
                return
            if self.filter.matches(item):
                self.__insert_item(item, self.sort_key)

    def __insert_item(self, item, sort_key) -> None:
        items = self.__items
        if sort_key is not None:
            sort_operator = operator.gt if self.sort_reverse else operator.lt
            before_index = self.__find_sorted_index_for_item(item, items, sort_key, sort_operator)
        else:
            before_index = self.__find_unsorted_index_for_item(item, self._get_master_items(), self.filter)
        self.__items.insert(before_index, item)
        self.begin_changes_event.fire(self.__items_key)
        self.notify_insert_item(self.__items_key, item, before_index)
        self.end_changes_event.fire(self.__items_key)
        # only update the selection here if there is no end changes event listener.
        # if there is a listener, updating the selection is done in end changes.
        self.__selection_changes.append((True, before_index))
        if not self.__end_changes_event_listener:
            for selection in self.__selections:
                selection.insert_index(before_index)

    def __remove_item(self, item):
        item_index = self.__items.index(item)
        del self.__items[item_index]
        self.begin_changes_event.fire(self.__items_key)
        self.notify_remove_item(self.__items_key, item, item_index)
        self.end_changes_event.fire(self.__items_key)
        # only update the selection here if there is no end changes event listener.
        # if there is a listener, updating the selection is done in end changes.
        self.__selection_changes.append((False, item_index))
        if not self.__end_changes_event_listener:
            for selection in self.__selections:
                selection.remove_index(item_index)

    # thread safe
    def __removed_master_item(self, index, item):
        """
            Subclasses can call this to notify this object that a item in
            the master item list has been removed.
        """
        with self._update_mutex:
            if self.__change_level > 0:
                return
            if item in self.__items:
                self.__remove_item(item)

    # thread safe
    def __updated_master_item(self, item):
        """
            Subclasses can call this to notify this object that a item in
            the master item list has been updated.
        """
        with self._update_mutex:
            if self.__change_level > 0:
                return
            items = self.__items
            if self.filter.matches(item):
                # item will be in the list
                sort_key = self.sort_key
                if sort_key is not None:
                    # are items sorted?
                    sort_operator = operator.gt if self.sort_reverse else operator.lt
                    before_index = self.__find_sorted_index_for_item(item, items, sort_key, sort_operator)
                    if item in items:
                        # item already in list?
                        index = items.index(item)
                        if before_index < index:
                            self.__removed_master_item(index, item)
                            self.__inserted_master_item(before_index, item)
                        elif before_index > index:
                            self.__removed_master_item(index, item)
                            self.__inserted_master_item(before_index - 1, item)
                    else:
                        # item is not in list, just insert
                        self.__inserted_master_item(before_index, item)
                else:
                    # items are not sorted
                    if not item in items:
                        # item is not in list, just insert. the before_index we pass will not be used so just pass 0
                        self.__inserted_master_item(0, item)
            else:
                # item will not be in list
                if item in items:
                    # item already in list
                    index = items.index(item)
                    self.__removed_master_item(index, item)

    # thread safe.
    def __build_items(self):
        """Build the items from the master items list.

        This method is thread safe.

        Builds the items from the master list by sorting them and then
         filtering them.
        """
        master_items = self._get_master_items()
        assert len(set(master_items)) == len(master_items)
        # sort the master item list. this is optional since it may be sorted downstream.
        if self.sort_key:
            master_items.sort(key=self.sort_key, reverse=self.sort_reverse)
        # construct the items list by expanding each master item to
        # include its children
        items = list()
        for item in master_items:
            # apply filter
            if self.filter.matches(item):
                # add item and its dependent items
                items.append(item)
        return items

    # thread safe.
    def __update_items(self):
        """Build the items and generate change messages.

        Builds the items from the master item list, then generates a sequence of
         inserter and remover calls representing the changes from the previous list.
        """
        with self._update_mutex:
            if self.__change_level > 0:
                return
            # first build the new items list, including items with master item.
            old_items = copy.copy(self.__items)
            items = self.__build_items()
            # now generate the insert/remove instructions to make the official
            # list match the proposed list.
            assert len(set(self._get_master_items())) == len(self._get_master_items())
            assert len(set(items)) == len(items)
            # this is a time critical algorithm; leave the timing code in here for
            # easy testing.
            # import time
            # t0 = time.perf_counter()
            self.begin_changes_event.fire(self.__items_key)
            if self.__items_sorted:
                old_sort_reverse = self.__sort_reverse
                sort_key = self.sort_key
                if not sort_key:
                    indexes = {item: index for index, item in enumerate(items)}
                    sort_key = lambda x: indexes[x]
                    self.__sort_reverse = False
                old_items_set = set(old_items)
                new_items_set = set(items)
                insert_items_set = new_items_set - old_items_set
                remove_items_set = old_items_set - new_items_set
                # remove old items by iterating through all and checking whether in remove items set
                for index, item in enumerate(old_items):
                    if item in remove_items_set:
                        self.__remove_item(item)
                # insert using sorting
                for item in insert_items_set:
                    self.__insert_item(item, sort_key)
                self.__sort_reverse = old_sort_reverse
            else:
                # requires sorting and not already sorted or not sorted: fall back to full replacement
                for item in old_items:
                    # remove all items
                    self.__remove_item(item)
                indexes = {item: index for index, item in enumerate(items)}
                sort_key = lambda x: indexes[x]
                old_sort_reverse = self.__sort_reverse
                self.__sort_reverse = False
                for item in items:
                    self.__insert_item(item, sort_key)
                self.__sort_reverse = old_sort_reverse
            self.__items_sorted = True
            self.end_changes_event.fire(self.__items_key)
            # t1 = time.perf_counter()
            # print(f"{int(1000000 * (t1 - t0))}us {len(self.__items)}")

    # thread safe.
    @property
    def container(self):
        return self.__container

    # thread safe.
    @container.setter
    def container(self, container):
        if self.__container:
            self.__item_inserted_event_listener.close()
            self.__item_inserted_event_listener = None
            self.__item_removed_event_listener.close()
            self.__item_removed_event_listener = None
            if self.__begin_changes_event_listener:
                self.__begin_changes_event_listener.close()
                self.__begin_changes_event_listener = None
            if self.__end_changes_event_listener:
                self.__end_changes_event_listener.close()
                self.__end_changes_event_listener = None
            if self.__reset_list_event_listener:
                self.__reset_list_event_listener.close()
                self.__reset_list_event_listener = None
            for item in reversed(copy.copy(self._get_master_items())):
                self.__item_removed(self.__master_items_key, item, len(self._get_master_items()) - 1)
        self.__container = container
        self.__items_sorted = False
        self.reset_list_event.fire(self.__items_key)
        if self.__container:
            self.__item_inserted_event_listener = self.__container.item_inserted_event.listen(self.__item_inserted)
            self.__item_removed_event_listener = self.__container.item_removed_event.listen(self.__item_removed)
            if hasattr(self.__container, "begin_changes_event") and hasattr(self.__container, "end_changes_event"):

                def begin_changes(key):
                    if key == self.__master_items_key:
                        self.begin_changes_event.fire(self.__items_key)

                def end_changes(key):
                    if key == self.__master_items_key:
                        self.end_changes_event.fire(self.__items_key)
                    for selection in self.__selections:
                        selection_copy = copy.copy(selection)
                        for do_insert, index in self.__selection_changes:
                            # adjust the selection copy for the new index, but don't add/remove the new index itself.
                            # leaves the selected items the same.
                            if do_insert:
                                selection_copy.insert_index(index)
                            else:
                                selection_copy.remove_index(index)
                        selection.set_multiple(selection_copy.indexes)
                    self.__selection_changes = list()

                self.__begin_changes_event_listener = self.__container.begin_changes_event.listen(begin_changes)
                self.__end_changes_event_listener = self.__container.end_changes_event.listen(end_changes)
            if hasattr(self.__container, "reset_list_event"):

                def reset_list(key):
                    self.__items_sorted = False
                    self.reset_list_event.fire(self.__items_key)

                self.__reset_list_event_listener = self.__container.reset_list_event.listen(reset_list)
            for index, item in enumerate(getattr(self.__container, self.__master_items_key)):
                self.__item_inserted(self.__master_items_key, item, index)

    def make_selection(self) -> Selection.IndexedSelection:
        selection = Selection.IndexedSelection()
        self.__selections.append(selection)
        return selection

    def release_selection(self, selection):
        self.__selections.remove(selection)

    # thread safe.
    def __item_inserted(self, key, item, before_index):
        """ Insert the master item. Called from the container. """
        if key == self.__master_items_key:
            with self._update_mutex:
                assert not item in self.__master_items
                self.__master_items.insert(before_index, item)

                # thread safe
                def item_content_changed():
                    with self._update_mutex:
                        assert item in self.__master_items
                        self.__updated_master_item(item)

                self.__item_changed_event_listeners.insert(before_index, item.item_changed_event.listen(item_content_changed) if hasattr(item, "item_changed_event") else None)
                self.__inserted_master_item(before_index, item)

    # thread safe.
    def __item_removed(self, key, item, index):
        """ Remove the master item. Called from the container. """
        if key == self.__master_items_key:
            with self._update_mutex:
                del self.__master_items[index]
                if self.__item_changed_event_listeners[index]:
                    self.__item_changed_event_listeners[index].close()
                del self.__item_changed_event_listeners[index]
                self.__removed_master_item(index, item)


class MappedListModel(Observable.Observable):

    def __init__(self, *, container=None, master_items_key: str=None, items_key: str=None, map_fn: typing.Callable=None, unmap_fn: typing.Callable=None, selection: Selection.IndexedSelection=None):
        super().__init__()
        self.__container = None
        self.__master_items_key = master_items_key
        self.__items_key = items_key
        self.__map_fn = map_fn or (lambda x: x)
        self.__unmap_fn = unmap_fn or (lambda x: x)
        self.__items : typing.List = list()  # a list of transformed items
        self._update_mutex = threading.RLock()
        self.__change_level = 0
        self.begin_changes_event = Event.Event()
        self.end_changes_event = Event.Event()
        self.__item_inserted_event_listener = None
        self.__item_removed_event_listener = None
        self.__begin_changes_event_listener = None
        self.__end_changes_event_listener = None
        self.__selections = list()
        if selection:
            self.__selections.append(selection)
        self.container = container

    def close(self):
        self.container = None
        self.__map_fn = None
        self.__unmap_fn = None

    def begin_change(self):
        """ Begin a set of changes. Balance with end_changes. """
        if self.__change_level == 0:
            self.begin_changes_event.fire(self.__items_key)
        self.__change_level += 1

    def end_change(self):
        """ End a set of changes and update items if finished. """
        with self._update_mutex:
            self.__change_level -= 1
            if self.__change_level == 0:
                self.end_changes_event.fire(self.__items_key)

    def changes(self):
        """ Acquire this while setting filter or sort so that changes get made simultaneously. """

        class ChangeTracker:
            def __init__(self, list_model: MappedListModel):
                self.list_model = list_model

            def __enter__(self):
                self.list_model.begin_change()
                return self

            def __exit__(self, type_, value, traceback):
                self.list_model.end_change()

        return ChangeTracker(self)

    def mark_changed(self) -> None:
        with self.changes(): pass

    @property
    def items(self) -> typing.Sequence:
        """ Return the items. """
        with self._update_mutex:
            return copy.copy(self.__items)

    @property
    def items_key(self):
        return self.__items_key

    def __getattr__(self, item):
        if item == self.__items_key:
            return self.items
        raise AttributeError()

    # thread safe.
    @property
    def container(self):
        return self.__container

    # thread safe.
    @container.setter
    def container(self, container):
        # remove old master items
        if self.__container:
            self.__item_inserted_event_listener.close()
            self.__item_inserted_event_listener = None
            self.__item_removed_event_listener.close()
            self.__item_removed_event_listener = None
            if self.__begin_changes_event_listener:
                self.__begin_changes_event_listener.close()
                self.__begin_changes_event_listener = None
            if self.__end_changes_event_listener:
                self.__end_changes_event_listener.close()
                self.__end_changes_event_listener = None
            for item in reversed(copy.copy(getattr(self.__container, self.__master_items_key))):
                self.__master_item_removed(self.__master_items_key, item, len(self.__items) - 1)
        # add new master items
        self.__container = container
        if self.__container:
            self.__item_inserted_event_listener = self.__container.item_inserted_event.listen(self.__master_item_inserted)
            self.__item_removed_event_listener = self.__container.item_removed_event.listen(self.__master_item_removed)
            if hasattr(self.__container, "begin_changes_event") and hasattr(self.__container, "end_changes_event"):

                def begin_changes(key):
                    if key == self.__master_items_key:
                        self.begin_change()

                def end_changes(key):
                    if key == self.__master_items_key:
                        self.end_change()

                self.__begin_changes_event_listener = self.__container.begin_changes_event.listen(begin_changes)
                self.__end_changes_event_listener = self.__container.end_changes_event.listen(end_changes)
            for index, item in enumerate(getattr(self.__container, self.__master_items_key)):
                self.__master_item_inserted(self.__master_items_key, item, index)

    def make_selection(self):
        selection = Selection.IndexedSelection()
        self.__selections.append(selection)
        return selection

    def release_selection(self, selection):
        self.__selections.remove(selection)

    # thread safe.
    def __master_item_inserted(self, key, item, before_index):
        """ Insert the item. Called from the container. """
        if key == self.__master_items_key:
            with self._update_mutex:
                mapped_item = self.__map_fn(item)
                self.__items.insert(before_index, mapped_item)
                self.notify_insert_item(self.__items_key, mapped_item, before_index)
                for selection in self.__selections:
                    selection.insert_index(before_index)

    # thread safe.
    def __master_item_removed(self, key, item, index):
        """ Remove the item. Called from the container. """
        if key == self.__master_items_key:
            with self._update_mutex:
                mapped_item = self.__items[index]
                if callable(self.__unmap_fn):
                    self.__unmap_fn(mapped_item)
                del self.__items[index]
                self.notify_remove_item(self.__items_key, mapped_item, index)
                for selection in self.__selections:
                    selection.remove_index(index)


class FlattenedListModel(Observable.Observable):
    """A flattened list model (list of lists).

    Watches child items in the master items in the container and flattens them into a list.
    """

    def __init__(self, *, container=None, master_items_key: str=None, child_items_key: str=None, items_key: str=None, selection: Selection.IndexedSelection=None):
        super().__init__()
        self.__container = None
        self.__master_items_key = master_items_key
        self.__child_items_key = child_items_key
        self.__items_key = items_key if items_key else child_items_key
        self.__master_items : typing.List = list()  # a list of master items (to be transformed)
        self.__items : typing.List = list()  # a list of flattened items
        self.__children : typing.Dict[typing.Any, typing.List] = dict()  # map master item to children
        self._update_mutex = threading.RLock()
        self.__item_inserted_event_listener = None
        self.__item_removed_event_listener = None
        self.__child_item_inserted_event_listener : typing.Dict = dict()
        self.__child_item_removed_event_listener : typing.Dict = dict()
        self.__selections = list()
        if selection:
            self.__selections.append(selection)
        self.container = container

    def close(self):
        self.container = None

    @property
    def items(self) -> typing.Sequence:
        """ Return the items. """
        with self._update_mutex:
            return copy.copy(self.__items)

    def __getattr__(self, item):
        if item == self.__items_key:
            return self.items
        raise AttributeError()

    # thread safe.
    @property
    def container(self):
        return self.__container

    # thread safe.
    @container.setter
    def container(self, container):
        # remove old master items
        if self.__container:
            self.__item_inserted_event_listener.close()
            self.__item_inserted_event_listener = None
            self.__item_removed_event_listener.close()
            self.__item_removed_event_listener = None
            for item in reversed(copy.copy(getattr(self.__container, self.__master_items_key))):
                self.__master_item_removed(self.__master_items_key, item, len(self.__master_items) - 1)
        # add new master items
        self.__container = container
        if self.__container:
            self.__item_inserted_event_listener = self.__container.item_inserted_event.listen(self.__master_item_inserted)
            self.__item_removed_event_listener = self.__container.item_removed_event.listen(self.__master_item_removed)
            for index, item in enumerate(getattr(self.__container, self.__master_items_key)):
                self.__master_item_inserted(self.__master_items_key, item, index)

    def make_selection(self):
        selection = Selection.IndexedSelection()
        self.__selections.append(selection)
        return selection

    def release_selection(self, selection):
        self.__selections.remove(selection)

    # almost thread safe. assumes child items will not change duing this call.
    def __master_item_inserted(self, key, item, before_index):
        # insert a master item.
        # set up listeners for child item changes.
        # add any existing child item.
        if key == self.__master_items_key:
            with self._update_mutex:
                assert not item in self.__master_items, "master item already in " + str(self.__master_items_key) + " (" + str(self.__items_key) + " / " + str(self.__child_items_key) + ")"
                # print(f"{self} inserted {item} {before_index} ({len(getattr(item, self.__child_items_key))})")
                self.__master_items.insert(before_index, item)
                self.__child_item_inserted_event_listener[item] = item.item_inserted_event.listen(functools.partial(self.__child_item_inserted, item))
                self.__child_item_removed_event_listener[item] = item.item_removed_event.listen(functools.partial(self.__child_item_removed, item))
                for index, child_item in enumerate(getattr(item, self.__child_items_key)):
                    self.__child_item_inserted(item, self.__child_items_key, child_item, index)

    # thread safe.
    def __master_item_removed(self, key, item, index):
        # remove a master item.
        # remove any existing child items.
        # remove listeners for child items.
        if key == self.__master_items_key:
            with self._update_mutex:
                for index_, child_item in reversed(list(enumerate(getattr(item, self.__child_items_key)))):
                    self.__child_item_removed(item, self.__child_items_key, child_item, index_)
                # print(f"{self} removed {item} {index} ({len(getattr(item, self.__child_items_key))})")
                del self.__master_items[index]
                del self.__child_item_inserted_event_listener[item]
                del self.__child_item_removed_event_listener[item]
                assert not item in self.__master_items, "master item still in " + str(self.__master_items_key) + " (" + str(self.__items_key) + " / " + str(self.__child_items_key) + ")"

    def __child_item_inserted(self, master_item, key, item, before_index):
        if key == self.__child_items_key:
            master_index = 0
            for master_item_ in self.__master_items:
                if master_item_ == master_item:
                    break
                master_index += len(self.__children.get(master_item_, list()))
            master_index += before_index
            self.__children.setdefault(master_item, list()).insert(before_index, item)
            self.__items.insert(master_index, item)
            self.notify_insert_item(self.__items_key, item, master_index)
            for selection in self.__selections:
                selection.insert_index(before_index)

    def __child_item_removed(self, master_item, key, item, index):
        if key == self.__child_items_key:
            master_index = 0
            for master_item_ in self.__master_items:
                if master_item_ == master_item:
                    break
                master_index += len(self.__children.get(master_item_, list()))
            master_index += index
            del self.__children[master_item][index]
            del self.__items[master_index]
            self.notify_remove_item(self.__items_key, item, master_index)
            for selection in self.__selections:
                selection.remove_index(master_index)


class ListPropertyModel(Observable.Observable):
    """Treat a list as a single value property.

    Watches for changes to the list and fires property changed events.

    Does not currently handle item content changes.
    """

    def __init__(self, list_model):
        super().__init__()
        self.__list_model = list_model
        self.__item_inserted_event_listener = list_model.item_inserted_event.listen(self.__item_inserted)
        self.__item_removed_event_listener = list_model.item_removed_event.listen(self.__item_removed)

    def close(self) -> None:
        self.__list_model = None
        self.__item_inserted_event_listener = None
        self.__item_removed_event_listener = None

    def __item_inserted(self, key: str, item, before_index: int) -> None:
        self.notify_property_changed("value")

    def __item_removed(self, key: str, item, index: int) -> None:
        self.notify_property_changed("value")

    @property
    def value(self):
        return self.__list_model.items
