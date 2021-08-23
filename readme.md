<div>
	<img
		src="static/mitsu.png"
		alt="mitsu"
		width="100px"
		height="100px"
	/>
</div>

# Mitsu Web API

A web API for censoring AniList adult media covers, banners, thumbnails and generating
AniList style character thumbnails.

## Demo

<div>
    <img 
        src="https://mitsu.0x16c3.com/filter/media/5081" 
        alt="Filtered thumbnail" 
        width="400"
    />
</div>

<div>
    <img 
        src="https://mitsu.0x16c3.com/character/57499" 
        alt="Character thumbnail" 
        width="400"
    />
</div>

## API Reference

#### Filter adult content

```http
  GET /filter/${mode}/${id}
```

| Parameter | Type     | Description                                                     |
| :-------- | :------- | :-------------------------------------------------------------- |
| `mode`    | `string` | \*Filtering mode, either `media`, `cover` or `banner`           |
| `id`      | `string` | \*AniList id of item. Specify type if using `cover` or `banner` |

    > Specify the type using this format: `ANIME-${id}` or `MANGA-${id}`

#### Get item

```http
  GET /character/${id}
```

| Parameter | Type  | Description                |
| :-------- | :---- | :------------------------- |
| `id`      | `int` | \*AniList id of character. |

## Run Locally

Clone the project

```bash
    git clone https://github.com/0x16c3/Mitsu-web
```

Go to the project directory

```bash
    cd Mitsu-web
```

Install dependencies

```bash
    pip install -r requirements.txt
```

Start the server

```bash
    py __init__.py
```
