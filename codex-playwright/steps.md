# Steps

- Opened `https://example.com`, confirmed "Example Domain" heading rendered, and followed the "More information..." link to IANA's Example Domains page.

## Network Requests

| Method | URL                                                        | Response              |
| ------ | ---------------------------------------------------------- | --------------------- |
| GET    | https://example.com/                                       | 200 OK                |
| GET    | https://www.iana.org/domains/example                       | 301 Moved Permanently |
| GET    | http://www.iana.org/help/example-domains                   | 307 Internal Redirect |
| GET    | https://www.iana.org/help/example-domains                  | 200 OK                |
| GET    | https://www.iana.org/_css/2025.01/iana_website.css         | 200 OK                |
| GET    | https://www.iana.org/_js/jquery.js                         | 200 OK                |
| GET    | https://www.iana.org/_js/iana.js                           | 200 OK                |
| GET    | https://www.iana.org/_img/2025.01/iana-logo-header.svg     | 200 OK                |
| GET    | https://www.iana.org/_img/2025.01/fonts/NotoSans-Latin.ttf | 200 OK                |
| GET    | https://www.iana.org/_img/bookmark_icon.ico                | 200 OK                |
