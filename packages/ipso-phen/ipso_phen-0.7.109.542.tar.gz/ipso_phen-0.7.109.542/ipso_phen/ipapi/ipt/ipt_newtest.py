from ipso_phen.ipapi.base.ipt_abstract import IptBase


import os
import logging

logger = logging.getLogger(os.path.splitext(__name__)[-1].replace(".", ""))


class IptNewtest(IptBase):
    def build_params(self):
        self.add_enabled_checkbox()

    def process_wrapper(self, **kwargs):
        wrapper = self.init_wrapper(**kwargs)
        if wrapper is None:
            return False

        res = False
        try:
            if self.get_value_of("enabled") == 1:
                img = wrapper.current_image

                # Write your code here
                wrapper.store_image(img, "current_image")
                res = True
            else:
                wrapper.store_image(wrapper.current_image, "current_image")
                res = True
        except Exception as e:
            res = False
            logger.error(f"NewTest FAILED, exception: {repr(e)}")
        else:
            pass
        finally:
            return res

    @property
    def name(self):
        return "NewTest"

    @property
    def package(self):
        return "Me"

    @property
    def is_wip(self):
        return True

    @property
    def real_time(self):
        return True

    @property
    def result_name(self):
        return "mask"

    @property
    def output_kind(self):
        return "mask"

    @property
    def use_case(self):
        return ["Pre processing"]

    @property
    def description(self):
        return """'Write your tool s description here. it will be used to generate documentation files"""
