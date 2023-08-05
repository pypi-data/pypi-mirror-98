[![](https://img.shields.io/pypi/v/foliantcontrib.apireferences.svg)](https://pypi.org/project/foliantcontrib.apireferences/)  [![](https://img.shields.io/github/v/tag/foliant-docs/foliantcontrib.apireferences.svg?label=GitHub)](https://github.com/foliant-docs/foliantcontrib.apireferences)

# APIReferences Preprocessor for Foliant

> APIReferences is a successor of APILinks preprocessor with slightly changed configuration syntax and completely rewritten insides. APILinks is now deprecated, please use APIReferences instead.

Preprocessor replaces API *reference*s in markdown files with links to corresponding method description on the API documentation web-page.

## What is it for?

Say, you have API documentation hosted at the url http://example.com/api-docs

It may be a [Swagger UI](https://swagger.io/tools/swagger-ui/) website or just some static one-page site (like [Slate](https://github.com/slatedocs/slate)).

If you have a site with API docs, you probably reference them from time in your other documents:

```
To authenticate user use API method `POST /user/authenticate`.
```

We thought, how cool it'd be if this fragment: **\`POST /user/authenticate\`** automatically transformed into a URL of this method's description on your API docs website:

```
To authenticate user use API method [POST user/authenticate](http://example.com/api-docs/#post-user-authenticate).
```

That's exactly what APIReferences does.

## How does it work?

The purpose of APIReferences is to convert references into links. In the example above \``POST /user/authenticate`\` is a reference, and `[POST user/authenticate](http://example.com/api-docs/#post-user-authenticate)` is a Markdown link, the result of APIReferences' work.

The resulting link URL (http://example.com/api-docs/#get-user-authenticate) always consists of two parts: `{url}{anchor}`. `url` is static and is set in config, but `anchor` differs for each method. Open your API documentation website and look for HTML elements with `id` attribute near method description sections. When you add this `id` to the website's URL with number sign # (we call this combination an *anchor*), your browser scrolls the page to this exact element.

The tricky part is to determine which anchor should be added to the website's URL for each method. APIReferences offers several ways to do that, we call these ways *modes* (which are supplied in the `mode` parameter). It's up to you to choose the most suitable mode for your API website.

Here are available modes with their short descriptions. Detailed descriptions and examples are in the **User Guide** below.

**1. Generating anchors**

Mode option: `generate_anchor`

Convert reference into an anchor without checking the website.

**2. Find anchor**

Mode option: `find_by_anchor`

Parse API website and collect all ids from specific tags. Then convert reference into an anchor and check whether the converted anchor is present among these ids.

**3. Find tag content**

Mode option: `find_by_tag_content`

This mode searches not by tag ids but by tag content (`<tag id="id">content</tag>`) Parse API website and collect all tags from the specified list, which have ids and text content. The content to search is constructed from the reference. If the tag is found, return a link to its id.

**4. Find method in swagger spec for SwaggerUI**

Mode option: `find_for_swagger`

Parse the swagger spec file and find the referenced method. The anchor is then constructed by a template. This mode will work for SwaggerUI websites.

**5. Find method in swagger spec for Redoc**

Mode option: `find_for_redoc`

Parse the swagger spec file and find the referenced method. The anchor is then constructed by a template. This mode will work for Redoc websites.

***

APIReferences is a highly customizable preprocessor. You can tune almost anything about reference conversion.

For details look through the following sections.

Glossary:

- **reference** — reference to an API method in the source file. The one to be replaced with the link, e.g. `GET user/config`
- **verb** — HTTP method, e.g. `GET`, `POST`, etc.
- **command** — resource used to represent method on the API documentation webpage, e.g. `/service/healthcheck`.
- **endpoint prefix** — A prefix from server root to the command. If the command is `/user/status` and full resource is `/api/v0/user/satus` then the endpoint prefix should be stated `/api/v0`. In references you can use either full resource (`{endpoint_prefix}/{command}`) or just the command. APIReferences will sort it out for you.
- **output** — string, which will replace the *reference*.
- **tag content** — plain text between the tags, for example `<tag>Tag content</tag>`.
- **anchor** — web-element id with leading number sign, for example `#get-user-config`. Adding the anchor to the end of the web URL will make a browser scroll to the specified web element.
- **mode** — the way APIReferences will determine correct anchors to add to website URLs.

## Quick Recipes

### Recipe 1: find by tag content

We want reference \``GET /user/status`\` to be pointed at this element on our API website:

```html
<h2 id="get-user-status">Operation GET /user/status</h2>
```

Minimal sufficiant foliant.yml:

```yaml
preprocessors:
    apireferences:
        API:
            My-API:
                mode: find_by_tag_content
                url: http://example.com/api  # path to your API website
                content_template: 'Operation {verb} {command}'
```

\``GET /user/status`\` -> [GET /user/status](http://example.com/api#get-user-status)

### Recipe 2: find by tag id

The task is the same as in Recipe 1. We want reference \``GET /user/status`\` to be pointed at this element on our API website:

```html
<h2 id="get-user-status">Operation GET /user/status</h2>
```

Minimal sufficiant foliant.yml:

```yaml
preprocessors:
    apireferences:
        API:
            My-API:
                mode: find_by_anchor
                url: http://example.com/api  # path to your API website
                anchor_template: '{verb} {command}'
                anchor_converter: slate
```

\``GET /user/status`\` -> [GET /user/status](http://example.com/api#get-user-status)

### Recipe 3: generate tag id

The task is the same as in Recipes 1 and 2, but this time you don't have access to API website at the time of building foliant project. We want reference \``GET /user/status`\` to be pointed at this element on our API website:

```html
<h2 id="get-user-status">Operation GET /user/status</h2>
```

Minimal sufficiant foliant.yml:

```yaml
preprocessors:
    apireferences:
        API:
            My-API:
                mode: generate_anchor
                url: http://example.com/api  # path to your API website
                anchor_template: '{verb} {command}'
                anchor_converter: slate
```

\``GET /user/status`\` -> [GET /user/status](http://example.com/api#get-user-status)

### Recipe 4: find link for SwaggerUI

We have a SwaggerUI website and we need to find link to the method by reference \``GET /user/status`\``.

Method anchors on SwaggerUI consist of tag and operationId, both of which are not present in our reference. APIReferences can find them for you in the spec file. Let's assume that correct tag and operationId are `usertag` and `getStatus`.

Minimal sufficiant foliant.yml:

```yaml
preprocessors:
    apireferences:
        API:
            My-API:
                mode: generate_for_swagger
                url: http://example.com/swagger_ui  # path to your API website
                spec: !path swagger.json  # path or direct url to OpenAPI spec
```

\``GET /user/status`\` -> [GET /user/status](http://example.com/swagger_ui#/usertag/getStatus)


## Installation

```shell
$ pip install foliantcontrib.apireferences
```

## Config

To enable the preprocessor, add `apireferences` to `preprocessors` section in the project config:

```yaml
preprocessors:
  - apireferences
```

The preprocessor has a lot of options. For your convenience, the required options are marked *(required)*; and those options which are used in customization are marked *(optional)*. Most likely you will need just one or two of the latter.

```yaml
preprocessors:
- apireferences:
    targets:  # optional. default: []
        - site
    trim_if_targets: # optional. default: []
        - pdf
    prefix_to_ignore: Ignore  # optional
    warning_level: 2  # optional
    reference:  # optional
        - regex: *ref_pattern
          only_with_prefixes: false
          only_defined_prefixes: false
          output_template: '[{verb} {command}]({url})'
          trim_template: '`{verb} {command}`'
        - regex: *another_ref_pattern  # second reference config. Unlisted options are default
          output_template: '**{verb} {command}**'
    API:  # below are examples for each mode
        Client-API:  # reference prefix
            mode: generate_anchor
            url: http://example.com/api/client
            anchor_template: '{verb} {command}'
            anchor_converter: pandoc  # optional
            endpoint_prefix: /api/v1  # optional
        Admin-API:
            mode: find_by_anchor
            url: http://example.com/api/admin
            anchor_template: '{verb} {command}'
            anchor_converter: pandoc  # optional
            endpoint_prefix: /api/v1  # optional
            tags: ['h1', 'h2', 'h3', 'h4']  # optional
            login: login  # optional
            password: password  # optional
        External-API:
            mode: find_by_tag_content
            url: http://example.com/api/external
            content_template: '{verb} {command}'
            endpoint_prefix: /api/v1  # optional
            tags: ['h1', 'h2', 'h3', 'h4']  # optional
            login: login  # optional
            password: password  # optional
        Inernal-API:
            mode: find_for_swagger
            url: http://example.com/api/swagger-ui
            anchor_template: '/{tag}/{operation_id}'
            anchor_converter: no-transform
            endpoint_prefix: /api/v1  # optional
            login: login  # optional
            password: password  # optional
```

`targets`
:   *(optional)* List of supported targets for `foliant make` command. If target is not listed here — preprocessor won't be applied. If the list is empty — preprocessor will be applied for any target. Default: `[]`

`trim_if_targets`
:   *(optional)* List of targets for `foliant make` command for which the prefixes from all *references* in the text will be cut out. Default: `[]`

> Only those references whose prefixes are defined in the `API` section (described below) are affected by this option. All references with unlisted prefixes will not be trimmed.

`prefix_to_ignore`
:   *(optional)* A default prefix for ignoring references. If APIReferences meets a reference with this prefix it leaves it unchanged. Default: `Ignore`

`warning_level`
:   *(optional)* `2` — show all warnings for not found references; `1` — show only warnings for not found prefixed references; `0` — don't show warnings about not found references. Default: `2`

`reference`
:   *(optional)* List of dictionaries. A subsection for listing all the types of references you are going to catch in the text, and their properties. Options for this section are listed below.

> All reference properties have defaults. If any of them are missing in the config, the defaults will be used. If `reference` section is omitted, APIReferences will use default values.

***

**Reference options**

`regex`
:   *(optional)* regular expression used to catch *references* in the source. Look for details in the **Capturing References** section.
Default:

```
`((?P<prefix>[\w-]+):\s*)?(?P<verb>OPTIONS|GET|HEAD|POST|PUT|DELETE|TRACE|CONNECT|PATCH|LINK|UNLINK)\s+(?P<command>\S+)`
```

`only_with_prefixes`
:   *(optional)* if this is `true`, only *references* with prefix will be transformed. Ordinary links like `GET user/info` will be ignored. Default: `false`

`only_defined_prefixes`
:   *(optional)* if this is `true` all references whose prefix is not listed in the `API` section (described below) will be ignored. References without prefixes are not affected by this option. Default: `false`.

`output_template`
:   *(optional)* A template string describing the *output* which will replace the *reference*. More info in the **Customizing Output** section. Default: `'[{verb} {command}]({url})'`

`trim_template`
:   *(optional)* Only for targets listed in `trim_if_targets` option. Tune this template if you want to customize how APIReferences cuts out prefixes. The reference will be replaced with text based on this template. Default: ```'`{verb} {command}`'```

***

`API`
:   *(required)* A subsection for listing APIs and their properties. Define a separate subsection for each API here. The section name represents the API name and, at the same time, the *prefix* used in the references. You need to add at least one API subsection for the preprocessor to work.

**API properties**

The list of options and some default values differ for each mode.

`mode`
:   *(required)* API mode, which determines how references are collected. Available modes: `generate_anchor`, `find_by_anchor`, `find_by_tag_content`, `find_for_swagger`, `find_for_redoc`.


**`generate_anchor` mode**

`url`
:   *(required)* An API documentation web-page URL. It will be used to construct the full link to the method.

`anchor_template`
:   *(required)* A template string describing the format of the anchors in the API documentation web-page. You can use placeholders in {curly braces}, with names of the groups from the reference regex. Example: `'user-content {verb} {command}'`.

`anchor_converter`
:   *(optional)* anchor converter from [this list](https://github.com/foliant-docs/foliantcontrib.utils.header_anchors#to_id). Determines how string `GET /user/status` is converted into `get-userstatus` or `get-user-status` etc. [List of available converters](https://github.com/foliant-docs/foliantcontrib.utils.header_anchors#to_id). Default: `pandoc`

`endpoint_prefix`
:   *(optional)* The endpoint prefix from the server root to API methods. If is stated — APIReferences can divide the command in the reference and search for it more accurately. Also, you could use it in templates. More info in the **Commands and Endpoint Prefixes** section. Default: `''`

**`find_by_anchor` mode**

`url`
:   *(required)* An API documentation web-page URL. It will be used to construct the full link to the method. In this mode, it is also being parsed to check whether the generated anchor is present on the page.

`anchor_template`
:   *(required)* A template string describing the format of the anchors in the API documentation web-page. You can use placeholders in {curly braces}, with names of the groups in the reference regex. Example: `'user-content {verb} {command}'`.

`anchor_converter`
:   *(optional)* anchor converter from [this list](https://github.com/foliant-docs/foliantcontrib.utils.header_anchors#to_id). Determines how string `GET /user/status` is converted into `get-userstatus` or `get-user-status` etc. Default: `pandoc`

`endpoint_prefix`
:   *(optional)* The endpoint prefix from the server root to API methods. If is stated — APIReferences can divide the command in the reference and search for it more accurately. Also, you could use it in templates. More info in the **Commands and Endpoint Prefixes** section. Default: `''`

`tags`
:   *(optional)* list of HTML tags which will be parsed out from the page and searched for ids. Default: `['h1', 'h2', 'h3', 'h4']`

`login`
:    *(optional)* Login for basic authentication if present on your API site.

`password`
:    *(optional)* Password for basic authentication if present on your API site.

**`find_by_tag_content` mode**

`url`
:   *(required)* An API documentation web-page URL. It will be used to construct the full link to the method. In this mode, it is also being parsed to check whether the generated anchor is present on the page.

`content_template`
:   *(required)* A template string describing the format of the tag content in the API documentation web-page. You can use placeholders in {curly braces}, with names of the groups in the reference regex. Example: `'{verb} {command}'`.

`endpoint_prefix`
:   *(optional)* The endpoint prefix from the server root to API methods. If is stated — APIReferences can divide the command in the reference and search for it more accurately. Also you could use it in templates. More info in the **Commands and Endpoint Prefixes** section. Default: `''`

`tags`
:   *(optional)* list of HTML tags which will be parsed out from the page and searched for ids. Default: `['h1', 'h2', 'h3', 'h4']`

`login`
:    *(optional)* Login for basic authentication if present on your API site.

`password`
:    *(optional)* Password for basic authentication if present on your API site.

**`find_for_swagger` mode**

`url`
:   *(required)* An API documentation web-page URL. It will be used to construct the full link to the method.

`spec`
:   *(required)* URL or local path to OpenAPI specification file.

`anchor_template`
:   *(optional)* A template string describing the format of the anchors in the API documentation web-page. You can use placeholders in {curly braces}, with names of the groups in the reference regex. In this mode, you can also use two additional placeholders: `{tag}` and `{operation_id}`. Default: `'/{tag}/{operation_id}'`.

`endpoint_prefix`
:   *(optional)* The endpoint prefix from the server root to API methods. You may use it in output template. Default: `''`

`login`
:    *(optional)* Login for basic authentication if present on your API site.

`password`
:    *(optional)* Password for basic authentication if present on your API site.

**`find_for_redoc` mode**

`url`
:   *(required)* An API documentation web-page URL. It will be used to construct the full link to the method.

`spec`
:   *(required)* URL or local path to OpenAPI specification file.

`anchor_template`
:   *(optional)* A template string describing the format of the anchors in the API documentation web-page. You can use placeholders in {curly braces}, with names of the groups in the reference regex. In this mode, you can also use two additional placeholders: `{tag}` and `{operation_id}`. Default: `'operation/{operation_id}'`.

`endpoint_prefix`
:   *(optional)* The endpoint prefix from the server root to API methods. You may use it in output template. Default: `''`

`login`
:    *(optional)* Login for basic authentication if present on your API site.

`password`
:    *(optional)* Password for basic authentication if present on your API site.

# User guide

The purpose of APIReferences is to convert *references* into Markdown links. 

Reference is a chunk of text in your Markdown source which will be parsed by APIReferences, separated into groups, and converted into a link. An example of a reference is \``GET /user/authenticate`\`. APIReferences uses Regular Expressions to find the reference and split into groups. You can supply your own regular expression in `reference -> regex` param (details in **Capturing References** section below). If you are using the default one, the reference from the example above will be split into two groups:

- **verb**: `GET`,
- **command**: `/user/authenticate`.

These groups then will be used to find the referenced method on the API website and also to construct an *output string*.

For example, with `find_by_tag_content` mode (see the detailed description of all modes below) APIReferences will use `content_template` from API configuration to construct a tag content and search for it on the API website. If the content template is `'{verb} {command}'`, then the constructed content for the example above will be `GET /user/authenticate`. APIReferences will search for a tag with such content on the page and get its id.

The found tag may be `<h2 id="get-userauthenticate">GET /user/authenticate</h2>`. APIReferences will take the id from this tag and use it as an anchor to the link: `#get-userauthenticate`. Then it will add the API website path and here's your url: `http://example.com/api/#get-userauthenticate`.

Now, when APILink has the url of the method description, it can construct an output string. The output string is formed by a template, stated in reference `output_template` param. This template contains placeholders, which correspond to the reference groups with an addition of `{url}` placeholder, which contains the url formed above.

If the output template is `'[{verb} {command}]({url})'`, then the output string for our example will be:

`[GET /user/authenticate](http://example.com/api/#get-userauthenticate)`.

That's it, we've turned our reference into a Markdown link:

\``GET /user/authenticate`\` -> `[GET /user/authenticate](http://example.com/api/#get-userauthenticate)`.

That's the big picture. Now let's start with exploring different *modes* by means of which APIReferences captures references on API websites and transforms them into links.

## API Modes

As mentioned above, APIReferences takes a reference from your markdown source and splits it into groups. It then uses these groups to find the correct id on the API website. How this search is performed is determined by *API Mode*. It can search for a specific tag on the page by tag content or by its id; it can also search for the operation in an OpenAPI specification file or just construct an id without any checks, depending on the mode you've chosen. The mode is specified in `API -> <api name> -> mode` config option.

### `generate_anchor` mode

`generate_anchor` is the simplest mode. It just generates the anchor basing on the `anchor_template` parameter. It doesn't perform any checks on the API website and doesn't even require the website to be reachable at the time of building your Foliant project.

Let's assume that your API website code looks like this:

```html
...
<h2 id="user-content-get-userlogin">GET /user/status</h2>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>

<h2 id="user-content-get-apiv2adminstatus">GET /api/v2/admin/status</h2>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
...
```

APIReferences config in your `foliant.yml` in this case may look like this:

```yaml
preprocessors:
    apireferences:
        API:
            My-API:
                mode: generate_anchor
                url: http://example.com/api
                anchor_template: 'user content {verb} {command}'
                anchor_converter: pandoc
```

As you may have noticed, there's no `reference` section in the example above. That's because we will be using default values for the reference.

Now let's reference a **GET /user/status** method in our Markdown source:

```
To find out user's status use `My-API: GET /user/status` method.
```

> Note that for `generate_anchor` mode, the API prefix (`My-API` in our case) is required in the reference. More info about prefixes in **Handling Multiple APIs** section.

APIReferences will notice a reference mentioned in our markdown: \``My-API: GET /user/status`\`. It will capture it and split into three groups:

- **prefix**: `My-API`,
- **verb**: `GET`,
- **command**: `/user/status`.

Then it will pass it to the anchor template `'user content {verb} {command}'` which we've stated in our config, and this will result in a string:

`'user content GET /user/status'`

After that APIReferences will convert this string into an id with anchor converter. We've chosen `pandoc` converter in our config, which will turn the string into this: `user-content-getuserstatus`. That's exactly the id we needed, look an the webpage source:

```html
<h2 id="user-content-get-userstatus">GET /user/status</h2>
```

APIReferences will add this id to our API url (which we've stated in config) to form a link: `http://example.com/api#user-content-get-userstatus`.

Finally, it's time to construct a Markdown link. APIReferences takes an `output_template` from the reference config (which is omitted in our example foliant.yml because we are using defaults): `'[{verb} {command}]({url})'`.

Placeholders in the output template are replaced by groups from our reference, except `{url}` placeholder which is replaced with the url constructed above:

`[GET /user/status](http://example.com/api#user-content-get-userstatus)`

The conversion is done. Our Markdown content will now look like this:

```
To find out user's status use [GET /user/status](http://example.com/api#user-content-get-userstatus) method.
```

### `find_by_anchor` mode

`find_by_anchor` generates the id by `anchor_template` parameter and searches for this id on the API web page. If an element with such id is found, the reference is converted into a Markdown link. If not — the reference is skipped.

Let's assume that your API website code looks like this:

```html
...
<h2 id="api-method-get-userstatus">GET /user/status</h2>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>

<h2 id="api-method-get-apiv2adminstatus">GET /api/v2/admin/status</h2>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
...
```

APIReferences config in your `foliant.yml` in this case may look like this:

```yaml
preprocessors:
    apireferences:
        reference:
            output_template: '**[{verb} {command}]({url})**'
            # other reference properties are default
        API:
            My-API:
                mode: find_by_anchor
                url: http://example.com/api
                tags: ['h1', 'h2']
                anchor_template: 'api-method {verb} {command}'
                anchor_converter: pandoc
```

Now let's reference a **GET /user/status** method in our Markdown source:

```
To find out user's status use `GET /user/status` method.
```

APIReferences will notice a reference mentioned in our markdown: \``GET /user/status`\`. It will capture it and split into two groups:

- **verb**: `GET`,
- **command**: `/user/status`.

Then it will pass it to the anchor template `'api-method {verb} {command}'` which we've stated in our config, and this will result in a string:

`'user content GET /user/status'`

After that APIReferences will convert this string into an id with an anchor converter. We've used `pandoc` converter in our config, which will turn the string into this: `api-method-getuserstatus`.

Now APIReferences will parse the web page and look for all `h1` and `h2` tags (as specified in `tags` parameter) that have ids and compare these ids to our generated id.

One of the elements satisfies the requirement:

```html
<h2 id="api-method-get-userstatus">GET /user/status</h2>
```

It means that referenced method is present on API web page, so APIReferences will add this id to our API url (which we've stated in config) to form a link: `http://example.com/api#api-method-get-userstatus`.

Finally, it's time to construct a Markdown link. APIReferences takes an `output_template` from the reference config: `'**[{verb} {command}]({url})**'`.

Placeholders in the output template are replaced by groups from our reference, except `{url}` placeholder which is replaced with the url constructed above:

`**[GET /user/status](http://example.com/api#api-method-get-userstatus)**`

The conversion is done. Our Markdown content will now look like this:

```
To find out user's status use **[GET /user/status](http://example.com/api#api-method-get-userstatus)** method.
```

### `find_by_tag_content` mode

`find_by_tag_content` generates tag content by the `content_template` and searches for an HTML element with such content on the API web page. If an element is found, the reference is converted into a Markdown link. If not — the reference is skipped.

This mode is convenient when there's no way to determine tag id basing on the reference, for example, when ids are random strings.

Let's assume that your API website code looks like this:

```html
...
<h2 id="o1egwb7agw">GET /user/status</h2>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>

<h2 id="y3yn8ewg32">GET /api/v2/admin/status</h2>
<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
...
```

APIReferences config in your `foliant.yml` in this case may look like this:

```yaml
preprocessors:
    apireferences:
        reference:
            output_template: '[{prefix}: {verb} {command}]({url})'
            # other reference properties are default
        API:
            My-API:
                mode: find_by_tag_content
                url: http://example.com/api
                tags: ['h1', 'h2']
                content_template: '{verb} {command}'
```

Now let's reference a **GET /user/status** method in our Markdown source:

```
To find out user's status use `My-API: GET /user/status` method.
```

APIReferences will notice a reference mentioned in our markdown: \``My-API: GET /user/status`\`. The reference has the prefix `My-API`, which means that `My-API` from the `API` section should be used. It will capture it and split into three groups:

- **prefix**: `My-API`,
- **verb**: `GET`,
- **command**: `/user/status`.

Then it will pass it to the header template `'{verb} {command}'` which we've stated in our config, and this will result in a string:

`'GET /user/status'`

Now APIReferences will parse the web page and look for all `h1` and `h2` tags (as specified in the `tags` parameter) whose content equals to our generated content.

One of the elements satisfies the requirement:

```html
<h2 id="o1egwb7agw">GET /user/status</h2>
```

It means that referenced method is present on the API web page, so APIReferences will take an id `o1egwb7agw` from it and add it to our API url (which we've stated in config) to form a link: `http://example.com/api#o1egwb7agw`.

Finally, it's time to construct a Markdown link. APIReferences takes an `output_template` from the reference config: `'[{prefix}: {verb} {command}]({url})'`.

Placeholders in the output template are replaced by groups from our reference, except `{url}` placeholder which is replaced with the url constructed above:

`[My-API: GET /user/status](http://example.com/api#api-method-get-userstatus)`

The conversion is done. Our Markdown content will now look like this:

```
To find out user's status use [My-API: GET /user/status](http://example.com/api#api-method-get-userstatus) method.
```

### `find_for_swagger` mode

`find_for_swagger` mode parses the OpenAPI spec file and looks for the referenced method in it. It then generates an anchor for SwaggerUI website based on data from the reference and the operation properties in the spec.

Let's assume that your OpenAPI specification looks like this:

```json
{
    "swagger": "2.0",
    ...
    "paths": {
        "/user/status": {
            "GET": {
                "tags": ["userauth"],
                "summary": "Returns user auth status",
                "operationId": "checkStatus",
                ...
            },
        }
    ...

```

On the default SwaggerUI website the anchor to this method will be `#/userauth/checkStatus`. It consists of the first tag from the operation properties and the operationId. So to generate the proper anchor APIReferences will need to get those parts from the spec. 

APIReferences config in your `foliant.yml` in this case may look like this:

```yaml
preprocessors:
    apireferences:
        # reference options are default in this example
        API:
            My-API:
                mode: find_for_swagger
                url: http://example.com/api
                spec: !path swagger.json
                anchor_template: '/{tag}/{operation_id}'  # you can omit this line because it's the default value
```

Now let's reference a **GET /user/status** method in our Markdown source:

```
To find out user's status use `GET /user/login` method.
```

APIReferences will notice a reference mentioned in our markdown: \``GET /user/login`\`. It will capture it and split into two groups:

- **verb**: `GET`,
- **command**: `/user/login`.

> Note that `verb` and `command` groups are required for this mode if you are to redefine default reference regex.

Now, when we have a verb and a command, we can search for it in the OpenAPI spec. APIReferences parses the spec and searches the `paths` section for our operation. From the operation properties APIReferences takes two values: 

- **tag**: first element from the `tags` list,
- **operationId**.

These values are then passed to the anchor template `'/{tag}/{operation_id}'`, along with groups from our reference, this will result in a string:

`'/userauth/checkStatus'`

That's the id we were looking for. APIReferences will add it to our API url (which we've stated in config) to form a link: `http://example.com/api#/userauth/checkStatus`.

Finally, it's time to construct a Markdown link. APIReferences takes an `output_template` from the reference config, which is default: `'[{verb} {command}]({url})'`.

Placeholders in the output template are replaced by groups from our reference, except `{url}` placeholder which is replaced with the url constructed above:

`[GET /user/login](http://example.com/api#/userauth/checkStatus)`

The conversion is done. Our Markdown content will now look like this:

```
To find out user's status use [GET /user/login](http://example.com/api#/userauth/checkStatus) method.
```

### `find_for_redoc` mode

`find_for_redoc` is similar to `find_for_swagger` mode, except that deafult anchor template is `'operation/{operation_id}'`.

## Handling Multiple APIs

APIReferences can work with several APIs at once, and honestly, it's very good at this.

Let's consider an example foliant.yml:

```yaml
preprocessors:
    apireferences:
        API:
            Client-API:
                mode: find_by_tag_content
                url: http://example.com/api/client
                content_template: '{verb} {command}'
            Admin-API:
                mode: find_by_anchor
                url: http://example.com/api/admin
                content_template: '{verb} {command}'
```

In this example we've defined two APIs: `Client-API` and `Admin-API`, these are just names, they may be anything you want. Now we can reference both APIs:

```
When user clicks "LOGIN" button, the app sends a request `POST /user/login`.

To restrict user from logging in run `PUT /admin/ban_user/{id}`.
```

After applying the preprocessor, this source will turn into:

```
When user clicks "LOGIN" button, the app sends a request [POST /user/login](http://example.com/api/client#post-userlogin).

To restrict user from logging in run [PUT /admin/ban_user/{id}](](http://example.com/api/admin#put-adminbanuser-id).
```

As you see, APIReferences determined, which reference corresponds to which API. That is possible because when APIReferences meets a non-prefixed reference, it goes through each defined API and searches for the mentioned method.

But what happens if we reference a method which is present in both APIs?

```
Run `GET /system/healthcheck` for debug information.
```

You have to understand that, even though APIReferences is very powerful, it doesn't understand the concept of free will. It can't make the choice for you, so instead, it will show a warning and skip this reference:

```
WARNING: [index.md] Failed to process reference. Skipping. `GET /system/healthcheck` is present in several APIs (Client-API, Admin-API). Please, use prefix.
```

In the warning text, there's a suggestion to use a *prefix*. A prefix is a way to make your reference more specific and point APIReferences to the correct API. The value of the prefix is the API name as defined in the config. So for Client API, the prefix would be `Client-API`, for Admin — `Admin-API`. Let's fix our example:

```
Run `Admin-API: GET /system/healthcheck` to get debug information about the Admin API service.

Run `Client-API: GET /system/healthcheck` to get debug information about the Client API service.
```

> If you don't like the format in which we supply prefix (`<prefix>: <verb> <command>`), you can change it by tweaking reference regex. More info in **Capturing References** section.

It's recommended to always use prefixes for unambiguity. The `generate_anchor` mode won't work at all for references without prefixes, because it doesn't perform any checks and almost always returns a link.

## Handling Multiple Reference Configuration

You can not only make APIReferences work with different APIs but also with different reference configurations. `reference` parameter is a list for a reason. And because `output_template` is part of reference configuration, you can make different references transform into different values.

Here's an example config:

```yaml
preprocessors:
    apireferences:
        reference:
            - only_with_prefixes: true
              output_template: '**[{verb} {command}]({url})**'
            - only_with_prefixes: false
              output_template: '[{verb} {command}]({url})'
        API:
            ...
```

With such config references with prefixes will be transformed into **bold links**, while non-prefixed references will remain regular links.

## Commands and Endpoint Prefixes

APIReferences treats the `command` part of your reference in a special way. While searching for it on the API website it will try to substitute the command place holder:

- with and without leading slash (`/user/login` and `user/login`),
- with and without endpoint prefix, if one is defined (`/api/v1/user/login` and `/user/login`).

Here's an example config to illustrate this feature:

```yaml
preprocessors:
    apireferences:
        reference:
            - only_with_prefixes: true
              output_template: '**[{verb} {command}]({url})**'
            - only_with_prefixes: false
              output_template: '[{verb} {command}]({url})'
        API:
            My-API:
                mode: find_by_tag_content
                url: http://example.com/api
                content_template: '{verb} {command}'
                endpoint_prefix: /api/v1
```

Considering that the API website source looks like this:

```html
<h2 id="asoi17uo">GET /api/v1/user/status</h2>
```

Which of these references, do you think, will give us the desired result?

```
`GET /user/status`
`GET user/status`
`GET /api/v2/user/status`
```

If you were reading carefully, you already know the answer — all of these references will result in the same link:

```
[GET /user/status](http://example.com/api#asoi17uo)
[GET /user/status](http://example.com/api#asoi17uo)
[GET /user/status](http://example.com/api#asoi17uo)
```


# Capturing References

APIReferences uses regular expressions to capture *references* to API methods in Markdown files.

The default reg-ex is:

```re
`((?P<prefix>[\w-]+):\s*)?(?P<verb>OPTIONS|GET|HEAD|POST|PUT|DELETE|TRACE|CONNECT|PATCH|LINK|UNLINK)\s+(?P<command>\S+)`
```

This expression accepts references like these:

- `Client-API: GET user/info`
- `UPDATE user/details`

Notice that the default expression uses [Named Capturing Groups](https://docs.python.org/3/howto/regex.html#non-capturing-and-named-groups). You have to use them too if you are to redefine the expression. You can name these groups as you like and have as many or as few as you wish, but it's recommended to include the `prefix` group for API prefix logic to work. It is also required for all groups which are in the `output_template` also to be present in the regex.

To redefine the regular expression add an option `regex` to the reference config.

For example, if you want to capture ONLY references with prefixes you may use the following:

```yaml
preprocessors:
  - apireferences:
      reference:
      - regex: '((?P<prefix>[\w-]+):\s*)(?P<verb>POST|GET|PUT|UPDATE|DELETE)\s+(?P<command>\S+)`'
```

> This example is for illustrative purposes only. You can achieve the same goal by just switching on the `only_with_prefixes` option.

Now the references without prefix (`UPDATE user/details`) will be ignored.

# Customizing Output

You can customize the *output*-string which will replace the *reference* string. To do that add a template into your reference configuration.

A *template* is a string that may contain placeholders, surrounded by curly braces. These placeholders will be replaced with the values, and all the rest will remain unchanged.

For example, look at the default template:

```yaml
preprocessors:
  - apireferences:
    reference:
      - output_template: '[{verb} {command}]({url})',
```

> Don't forget the single quotes around the template. These braces and parenthesis easily make YAML think that it is an embedded dictionary or list.

With the default template, the reference string will be replaced by something like that:

```
[GET user/info](http://example.com/api/#get-user-info)
```

If you want references to be transformed into something else, create your own template. You can use placeholders from the reference regular expression along with some additional:

placeholder | description | example
-------- | ----------- | -------
source | Full original reference string | \``Client-API: GET user/info`\`
url | Full url to the method description | `http://example.com/api/#get-user-info`
endpoint_prefix | API endpoint prefix from API configuration | `/api/v2`

Placeholders from the default regex are:

placeholder | description | example
-------- | ----------- | -------
prefix | API Prefix used in the reference | `Client-API`
verb | HTTP verb used in the reference | `GET`
command | API command being referenced with endpoint prefix removed | `/user/info`
