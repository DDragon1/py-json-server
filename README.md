# Py-json-server  
This server is used to get and set jsons in a mongoDB and even randomize.
The DB is a mongoDB
You will need a **`mongoDB`** and a way to run `docker` / `python`

## Features  
- Get all of the items in a specific `api` (collection)
- Get a specific Json with a specific URL (data in a collection)
- Get a Json with randomize fields that have been configured in the input
- Randomizble fields - string, int, float, timestamp, GEO position, ENUMS, object
- Get an save the randomize response back in the mongoDB  
- Get a Json with a `fake` url, so you can add every URI or params at the end of it    

## Environment Variables  
To run this project, you will need to add the following environment variables to your .env file  
`MONGO_CONNECTION`  The connection string of the mongo, **default:** `mongodb://localhost:27017`

`MONGO_DB_NAME`  The name of the DB in the Mongo, **default:** `Shimon`


## Deployment  
To deploy this project run (don't forget the environment variables) 

```bash
  flask run --host=0.0.0.0
``` 

Or use run the docker image

```bash
  docker run --env MONGO_DB_NAME=test --env MONGO_CONNECTION=mongodb://localhost:27017 
  --name py-json-server py-json-server:2
```


## API Reference

#### Get all items for an API  

```http
  GET /all/<api>
  POST /all/<api>
```  

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api` | `string` | **Required**. The name of the collection |

#### Get item
```http
  GET /<api>/<name?>/<version?>
  POST /<api>/<name?>/<version?>
```  

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api`  | `string` | **Required**. The name of the collection |
| `name` | `string` | **Not Required**. The name of the item |
| `version` | `string` | **Not Required**. The version of the item |

~~~http
  POST add/<api>/<name?>/<version?>
~~~

| Parameter | Type     | Description                         | Default   |
| :-------- | :------- | :---------------------------------- | :-------- |
| `api`  | `string` | **Required**. The name of the collection | |
| `name` | `string` | **Not Required**. The name of the item |  'default' |
| `version` | `string` | **Not Required**. The version of the item   | '1' |

~~~http
  GET <api>/<name?>/<version?>/fake/<every string>
~~~

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `api`  | `string` | **Required**. The name of the collection |
| `name` | `string` | **Not Required**. The name of the item |
| `version` | `string` | **Not Required**. The version of the item |
| `every string` | `string` | **Not Required**. Whatever string and params you want |  
 

## Supported Randoms

### randomInt

Replaces the desired key's value with a random integer

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `min`   | `int` | `0` | The min value of the random |
| `max`  | `int` | `100` | The max value of the random |

~~~Json
"overrides": {
	"id": {
		"type": "randomInt",
		"params": {
			"min": 1,
			"max": 1000
		}
	}
}
~~~

### randomFloat

Replaces the desired key's value with a random float number

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `min`   | `float` | `0.0` | The min value of the random |
| `max`  | `float` | `100.0` | The max value of the random |
| `decPlace`  | `int` | `2` | The number of decimals to use when rounding the number |

~~~Json
"overrides": {
	"age": {
		"type": "randomFloat",
		"params": {
			"min": 0.0,
			"max": 120.0,
            "decPlace": 1
		}
	}
}
~~~

### randomString

Replaces the desired key's value with a randomize string from the input chars

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `size`   | `int` | `8` | The min value of the random |
| `chars`  | `sequence` | `printable` | A sequence like a list, a tuple, a range of numbers etc. |

`printable` - pre-initialized string in python. A set of punctuation, digits, ascii_letters and whitespace

**More premade sets:** (from string.pyi)
* ascii_letters
* ascii_lowercase
* ascii_uppercase
* capwords
* digits
* hexdigits
* octdigits
* printable
* punctuation
* whitespace
* Formatter
* Template

`chars` - can be a every string, not only the premade sets

~~~Json
"overrides": {
	"username": {
		"type": "randomString",
		"params": {
			"size": 10,
            "chars": "ascii_lowercase"
		}
	}
}
~~~

### randomGEO

Replaces the desired key's value with a randomize tuple of 2 float numbers

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `minX`   | `float` | `32.0` | The min value of the first elemnt |
| `maxX`  | `float` | `33.5` | The max value of the first elemnt |
| `minY`   | `float` | `35.0` | The min value of the second elemnt |
| `maxY`  | `float` | `36.5` | The max value of the second elemnt |

~~~Json
"overrides": {
	"location": {
		"type": "randomGEO",
		"params": {
			"minX": 33.3,
            "maxX": 34.2,
            "minY": 35.0,
            "maxY": 36.8
		}
	}
}
~~~

result example:
~~~Json
"location": [
	33.168916,
	35.172589
]
~~~
### randomTimestamp

Replaces the desired key's value with a randomize timestamp between the current time and the time with `delta` seconds before the current time

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `delta`   | `int` | `4` | The number of seconds before the cuurent time, the minimun random timestamp can be |

The calculation is random_between(`time.now().asSeconds()` - `delta`, `time.now()`)

~~~Json
"overrides": {
	"lastUpdateTime": {
		"type": "randomTimestamp",
		"params": {
			"delta": 4
		}
	}
}
~~~

### randomEnum

Replaces the desired key's value with a one of the elements in the input array

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `enums`   | `array` | `[]` | The elements that can be the desired value |

~~~Json
"favoriteColor": {
	"location": {
		"type": "randomEnum",
		"params": {
			"enums": [
                "green", "blue", "yellow", 1, 
                {
				"more": "black"
				}
            ]
		}
	}
}
~~~

### insertObject

Replaces the desired key's value with an object, can be used to insert an object to a certain key 

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `obj`   | `object` | `None` | The object that we want to set as the value |

~~~Json
"overrides": {
	"child": {
		"type": "insertObject",
		"params": {
			"obj": {
					"name": "son",
					"age": 12
				}
		}
	}
}
~~~

## Usage/Examples  
object in the <api> collection
~~~Json  
  {
	"name": "shimon",
	"version": "1",
	"data": {
		"action_name": "mobile signup",
		"functions": [{
			"name": "test_signUp",
			"parameters": {
				"username": "max@getappcard.com",
				"password": "12345",
				"mobileLater": "123454231",
				"mobile": "1e2w1e2w",
				"card": "1232313",
				"cardLater": "1234321234321"
			}
		}],
		"validations": [{
				"MOB_header": "My stores"
			},
			{
				"url": "/stores/my"
			}
		]
	},
	"overrides": {
		"username": {
			"type": "randomFloat",
			"params": {
				"min": 1,
				"max": 7,
				"decPlace": 2
			}
		}
	}
}
~~~  
 
## API Reference

#### Get all items for an API  

```http
  GET /all/<api>
  POST /all/<api>
```  

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api` | `string` | **Required**. The name of the collection |

#### Get item
```http
  GET /<api>/<name?>/<version?>
  POST /<api>/<name?>/<version?>
```  

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api`  | `string` | **Required**. The name of the collection |
| `name` | `string` | **Not Required**. The name of the item |
| `version` | `string` | **Not Required**. The version of the item |

~~~http
  POST add/<api>/<name?>/<version?>
~~~

| Parameter | Type     | Description                         | Default   |
| :-------- | :------- | :---------------------------------- | :-------- |
| `api`  | `string` | **Required**. The name of the collection | |
| `name` | `string` | **Not Required**. The name of the item |  'default' |
| `version` | `string` | **Not Required**. The version of the item   | '1' |

~~~http
  GET <api>/<name?>/<version?>/fake/<every string>
~~~

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `api`  | `string` | **Required**. The name of the collection |
| `name` | `string` | **Not Required**. The name of the item |
| `version` | `string` | **Not Required**. The version of the item |
| `every string` | `string` | **Not Required**. Whatever string and params you want |  
 

## Environment Variables  
To run this project, you will need to add the following environment variables to your .env file  
`MONGO_CONNECTION`  The connection string of the mongo, **default:** `mongodb://localhost:27017`

`MONGO_DB_NAME`  The name of the DB in the Mongo, **default:** `Shimon`


## Supported Randoms

### randomInt

Replaces the desired key's value with a random integer

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `min`   | `int` | `0` | The min value of the random |
| `max`  | `int` | `100` | The max value of the random |

~~~Json
"overrides": {
	"id": {
		"type": "randomInt",
		"params": {
			"min": 1,
			"max": 1000
		}
	}
}
~~~

### randomFloat

Replaces the desired key's value with a random float number

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `min`   | `float` | `0.0` | The min value of the random |
| `max`  | `float` | `100.0` | The max value of the random |
| `decPlace`  | `int` | `2` | The number of decimals to use when rounding the number |

~~~Json
"overrides": {
	"age": {
		"type": "randomFloat",
		"params": {
			"min": 0.0,
			"max": 120.0,
            "decPlace": 1
		}
	}
}
~~~

### randomString

Replaces the desired key's value with a randomize string from the input chars

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `size`   | `int` | `8` | The min value of the random |
| `chars`  | `sequence` | `printable` | A sequence like a list, a tuple, a range of numbers etc. |

`printable` - pre-initialized string in python. A set of punctuation, digits, ascii_letters and whitespace

**More premade sets:** (from string.pyi)
* ascii_letters
* ascii_lowercase
* ascii_uppercase
* capwords
* digits
* hexdigits
* octdigits
* printable
* punctuation
* whitespace
* Formatter
* Template

`chars` - can be a every string, not only the premade sets

~~~Json
"overrides": {
	"username": {
		"type": "randomString",
		"params": {
			"size": 10,
            "chars": "ascii_lowercase"
		}
	}
}
~~~

### randomGEO

Replaces the desired key's value with a randomize tuple of 2 float numbers

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `minX`   | `float` | `32.0` | The min value of the first elemnt |
| `maxX`  | `float` | `33.5` | The max value of the first elemnt |
| `minY`   | `float` | `35.0` | The min value of the second elemnt |
| `maxY`  | `float` | `36.5` | The max value of the second elemnt |

~~~Json
"overrides": {
	"location": {
		"type": "randomGEO",
		"params": {
			"minX": 33.3,
            "maxX": 34.2,
            "minY": 35.0,
            "maxY": 36.8
		}
	}
}
~~~

result example:
~~~Json
"location": [
	33.168916,
	35.172589
]
~~~
### randomTimestamp

Replaces the desired key's value with a randomize timestamp between the current time and the time with `delta` seconds before the current time

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `delta`   | `int` | `4` | The number of seconds before the cuurent time, the minimun random timestamp can be |

The calculation is random_between(`time.now().asSeconds()` - `delta`, `time.now()`)

~~~Json
"overrides": {
	"lastUpdateTime": {
		"type": "randomTimestamp",
		"params": {
			"delta": 4
		}
	}
}
~~~

### randomEnum

Replaces the desired key's value with a one of the elements in the input array

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `enums`   | `array` | `[]` | The elements that can be the desired value |

~~~Json
"favoriteColor": {
	"location": {
		"type": "randomEnum",
		"params": {
			"enums": [
                "green", "blue", "yellow", 1, 
                {
				"more": "black"
				}
            ]
		}
	}
}
~~~

### insertObject

Replaces the desired key's value with an object, can be used to insert an object to a certain key 

| Argument   | Type     | Default    | Description                       |
| :--------- | :------- | :---------: | :-------------------------------- |
| `obj`   | `object` | `None` | The object that we want to set as the value |

~~~Json
"overrides": {
	"child": {
		"type": "insertObject",
		"params": {
			"obj": {
					"name": "son",
					"age": 12
				}
		}
	}
}
~~~

## Usage/Examples  
object in the <api> collection
~~~Json  
{
  "_id": {
    "$oid": "6340384a7f4fab1902653301"
  },
  "name": "full",
  "version": "1",
  "data": {
    "action_name": "mobile signup",
    "info": [
      {
        "name": "test_signUp",
        "parameters": {
          "id": 12354,
          "username": "max@getappcard.com",
          "password": "12345",
          "mobileLater": "123454231",
          "mobile": "1e2w1e2w",
          "card": "1232313",
          "cardLater": "1234321234321",
          "age": 42.1,
          "lastUpdateTime": null,
          "location": [
            33.168916,
            35.172589
          ]
        }
      }
    ],
    "fields": [
      {
        "MOB_header": "My stores",
        "favoriteColor": "orange"
      },
      {
        "url": "/stores/my"
      }
    ],
    "child": "jhon"
  },
  "overrides": {
    "id": {
      "type": "randomInt",
      "params": {
        "min": 1,
        "max": 1000
      }
    },
    "username": {
      "type": "randomString",
      "params": {
        "size": 9,
        "chars": "ascii_lowercase"
      }
    },
    "password": {
      "type": "randomString",
      "params": {
        "size": 10
      }
    },
    "age": {
      "type": "randomFloat",
      "params": {
        "min": 13,
        "max": 99,
        "decPlace": 1
      }
    },
    "lastUpdateTime": {
      "type": "randomTimestamp",
      "params": {
        "delta": 10
      }
    },
    "location": {
      "type": "randomGEO",
      "params": {
        "minX": 33.3,
        "maxX": 34.2
      }
    },
    "favoriteColor": {
      "type": "randomEnum",
      "params": {
        "enums": [
          "green",
          "blue",
          "yellow",
          1,
          {
            "more": "black"
          }
        ]
      }
    },
    "child": {
      "type": "insertObject",
      "params": {
        "obj": {
          "name": "son",
          "age": 12
        }
      }
    }
  }
}
~~~  

An example respose to a request for that json:

~~~Json
{
	"action_name": "mobile signup",
	"child": {
		"age": 12,
		"name": "son"
	},
	"functions": [
		{
			"name": "test_signUp",
			"parameters": {
				"age": 56.6,
				"card": "1232313",
				"cardLater": "1234321234321",
				"id": 303,
				"lastUpdateTime": "2022-10-09T15:53:52.152303",
				"location": [
					33.168916,
					35.172589
				],
				"mobile": "1e2w1e2w",
				"mobileLater": "123454231",
				"password": "wsQLW\tcLxG",
				"username": "ctzqhbbwq"
			}
		}
	],
	"validations": [
		{
			"MOB_header": "My stores",
			"favoriteColor": "green"
		},
		{
			"url": "/stores/my"
		}
	]
}
~~~
 
## Run Locally  
Clone the project  

~~~bash  
  git clone https://github.com/DDragon1/py-json-server.git
~~~

Go to the project directory  

~~~bash  
  cd py-json-server
~~~

Install dependencies  

~~~bash  
pip install dnspython pymongo Flask
~~~

Start the server  

~~~bash  
flask run --host=0.0.0.0
~~~   
## Roadmap  
- [ ] save the current randroms so the ID's won't change 

- [ ] add changes by positions in tree