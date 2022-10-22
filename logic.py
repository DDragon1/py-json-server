import collections
import myRandoms 


def update_nested(in_dict: dict, overrides: dict, re_override: bool = False):
   for k, v in in_dict.items():
        if isinstance(v, dict):
            update_nested(v, overrides, re_override)
        elif isinstance(v, list):
            for o in v:
                if isinstance(o, dict):
                    update_nested(o, overrides, re_override)
        elif k in overrides:
            in_dict[k] = replacer(k, overrides, re_override, in_dict[k])


def replacer(key, overrides: dict, re_override: bool = False, value = None):
    if key in overrides:
        currDic = overrides[key]
        re_override = re_override and hasReOverride(currDic)
        if (re_override): 
            currDic = currDic.get('re-override')

        chosenType = currDic.get('type')
        params = currDic.get('params')
        try:
            if not re_override:
                result = myRandoms.RandomsEnums[chosenType](params)
            else:
                result = myRandoms.RelativeRandomsEnums[chosenType](value,params)
        except (TypeError,ValueError) as err:
            raise Exception("Failed to override key: {0}. Cause: {1}".format(key,err),500)
        except KeyError as err:
            raise Exception("There is no override function named {0}".format(key), 400)
        return result

def hasReOverride(curr_override: dict):
    return ('re-override' in curr_override)
