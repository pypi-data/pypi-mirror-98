import abc
import logging
from typing import List

__all__ = ['Ager']


class Ager():
    def __init__(self, **kwargs):
        self.logger = logging.getLogger("XIA.Ager")
        self.log_context = {'context': ''}
        if len(self.logger.handlers) == 0:
            formatter = logging.Formatter('%(asctime)s-%(process)d-%(thread)d-%(module)s-%(funcName)s-%(levelname)s-'
                                          '%(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    @classmethod
    def age_list_add_item(cls, age_list: List[list], item: list) -> List[list]:
        new_age_list, cur_item, start_point = list(), item.copy(), None
        for list_item in age_list:
            # <List Item> --- <New Item>
            if list_item[1] + 1 < cur_item[0]:
                new_age_list.append(list_item)
            # <New Item> --- <List Item>
            elif cur_item[1] + 1 < list_item[0]:
                new_age_list.append(cur_item)
                cur_item = list_item.copy()
            # <New Item && List Item>
            else:
                cur_item = [min(cur_item[0], list_item[0]), max(cur_item[1], list_item[1])]
        new_age_list.append(cur_item)
        return new_age_list

    @abc.abstractmethod
    def key_init(self, key: str, start_key: int):
        """Creating Ager Object for requested keys

        Attributes:
            key (:obj:`str`): object key (key should contains Target Topic, Target Table, Segment ID)
            start_key (:obj:`int`): Should be the start seq of header (+1)
        """

    @abc.abstractmethod
    def get_ready_age(self, key: str, start_key: int, end_key: int) -> int:
        """Adding age range and get the last ready age

        Attributes:
            key (:obj:`str`): object key (key should contains Target Topic, Target Table, Segment ID)
            start_key (:obj:`int`): new input start merge key
            end_key (:obj:`int`): new input end merge key

        Return:
            :obj:`int`: The end age number which is ready to be loaded (No GAP from beginning)
        """
