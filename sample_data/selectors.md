# Selectors Information

- Highest level post selector, prepend this to everything: `div.pt1.mb2.artdeco-card > div > div > div.feed-shared-update-v2 > div >`
  - Post URL: `Attr: data-urn`
  - Meta (Name, URL, Title and Date parent selector): `div.update-components-actor > div.update-components-actor__container > div.update-components-actor__meta >`
    - Author URL:
    `a[href] attr`
    - Author Name: `a > span.update-components-actor__title > span.update-components-actor__name > span > span:nth-of-type(1)`
    - Author Title: `a > span.update-components-actor__description > span:nth-of-type(1)`
    - Date: `a > span.update-components-actor__sub-description > div > span > span:nth-of-type(1)`
  - Post Text selector: `div.feed-shared-update-v2 > div > div:nth-of-type(4)`
  - Engagement selector: `div.update-v2-social-activity`
