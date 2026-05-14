# TeachAny Mini Program Wrapper

Use this wrapper to embed TeachAny H5 courseware in a WeChat Mini Program via `web-view`.

## Required Mini Program setup

1. Mini Program account must not be a personal account; personal accounts do not support `web-view`.
2. In Mini Program Admin → Development settings → Business domain, add the courseware domain:
   - `weponusa.github.io` or your own CNAME domain for TeachAny courseware.
3. Domain must be HTTPS and cannot be an IP address.
4. `web-view` automatically fills the page; each page can contain only one `web-view`.

## Usage

Open this page with a course id:

```text
/pages/courseware/courseware?id=hist-m-renaissance
```

It renders:

```text
https://weponusa.github.io/teachany-courseware/community/hist-m-renaissance/index.html#wechat_redirect
```

If you pass a full URL, encode it first:

```text
/pages/courseware/courseware?url=<encodeURIComponent(url)>
```

Only `https://weponusa.github.io/teachany-courseware/` URLs are accepted by the template.
