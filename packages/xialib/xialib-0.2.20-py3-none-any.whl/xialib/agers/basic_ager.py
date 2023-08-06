from datetime import datetime
from xialib.ager import Ager


class BasicAger(Ager):
    """Basic Ager Use Python dictionary (No persistence) as Age data holder

    """
    data = {}

    def get_ready_age(self, key: str, start_key: int, end_key: int) -> int:
        if key not in self.data:
            self.logger.error("Target {} has not been initialized".format(key), extra=self.log_context)
            raise ValueError("XIA-000035")
        ager_dict = self.data[key]
        current_frame_id = datetime.now().strftime("%Y%m%d%H%M%S")
        current_frame_list = ager_dict.get(current_frame_id, [])
        current_frame_list.append(str(start_key) + "-" + str(end_key))
        ager_dict[current_frame_id] = current_frame_list

        all_list, last_ok_frame = [], ""
        for frame_id in sorted(ager_dict):
            for item in ager_dict[frame_id]:
                all_list = self.age_list_add_item(all_list, [int(item.split("-")[0]), int(item.split("-")[1])])

        for frame_id in sorted(ager_dict):
            if all_list[0][-1] >= max([int(item.split("-")[-1]) for item in ager_dict[frame_id]]):
                last_ok_frame = frame_id

        # last_ok_frame could be empty if the ok frame contains gap
        if last_ok_frame:
            ager_dict[last_ok_frame].append(str(all_list[0][0]) + "-" + str(all_list[0][-1]))
            for frame_id in [id for id in sorted(ager_dict) if id < last_ok_frame]:
                if all_list[0][-1] >= max([int(item.split("-")[-1]) for item in ager_dict[frame_id]]):
                    ager_dict.pop(frame_id)
        return all_list[0][-1]

    def key_init(self, key: str, start_key: int):
        self.data[key] = {datetime.now().strftime("%Y%m%d%H%M%S"): [str(start_key) + "-" + str(start_key)]}
