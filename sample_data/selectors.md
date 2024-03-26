# Selectors Information

1. Highest level post selector:

`div.pt1.mb2.artdeco-card > div > div > div.feed-shared-update-v2 > div >`

    A. Post URL

    Attr: `data-urn`

    B. Meta: Name, URL, Title and Date parent selector:

    `div.update-components-actor > div.update-components-actor__container > div.update-components-actor__meta >`

        a. Author URL:

        a[href] attr

        b. Author Name:

        `span.update-components-actor__title > span.update-components-actor__name > span > span:nth-of-type(1)`

        c. Author Title:

        `span.update-components-actor__description > span:nth-of-type(1)`

        d. Date:

        `span.update-components-actor__sub-description > div > span:nth-of-type(1)`

    C. Post Text selector:

    `div.feed-shared-update-v2__description-wrapper`

    D. Engagement selector:

    `div.update-v2-social-activity`
