import collections
import myRandoms 


def update_nested(in_dict: dict, overrides: dict):
   for k, v in in_dict.items():
        if isinstance(v, dict):
            update_nested(v, overrides)
        elif isinstance(v, list):
            for o in v:
                if isinstance(o, dict):
                    update_nested(o, overrides)
        elif k in overrides:
            in_dict[k] = replacer(k, overrides)


def replacer(key, overrides: dict) :
    if key in overrides:
        currDic = overrides[key]
        chosenType = currDic['type']
        params = currDic['params']
        #print ("replacing " + key + " with " + chosenType + " using params: ")
        #print(params)
        try:
            result = myRandoms.RandomsEnums[chosenType](params)
        except (TypeError,ValueError) as err:
            raise Exception("Failed to override key: {0}. Cause: {1}".format(key,err),err)
        #print("randrom result = " + str(result))
        return result