https://www.geeksforgeeks.org/scrape-linkedin-using-selenium-and-beautiful-soup-in-python/

# Todo

# Row Selector
`div.feed-shared-update-v2`

# Post Date
- [x] Selector: `div.update-components-actor div.update-components-actor__meta.relative span.update-components-actor__sub-description`
- [ ] Keep everything before keyword ` •` and transform dates

# Post URL
- [x] Select attribute `data-urn`
- [x] Add keyword before result: `https://www.linkedin.com/feed/update/`

# Author/Company Name
- [x] Selector: `div.update-components-actor span.update-components-actor__name span.visually-hidden`

# Author Title
- [x] Selector: `div.update-components-actor span.update-components-actor__description span.visually-hidden`
- [x] Replace Regex with Value: `/\d+\,*\d+\Wfollowers/gm`

# Author/Company Profile URL
- [x] Extract URL from `div.update-components-actor.display-flex.update-components-actor--with-control-menu div.update-components-actor__container > a`
- [x] Split on keyword `?` and take nth value of `1`

# Company Followers
- [x] Selector `div.update-components-actor span.update-components-actor__description span.visually-hidden`
- [x] Replace regex `/(^\D*)/gm` with value ``
- [x] Keep everything before keyword `followers`

# Post Text
- [X] Selector `span.break-words span`

# Post Likes
- [X] Selector `.social-details-social-counts__item.social-details-social-counts__reactions.social-details-social-counts__reactions--left-aligned`
- [x] Split on keyword ` ` and take nth value `1`

# Comments
- [X] Selector `li.social-details-social-counts__item.social-details-social-counts__comments`
- Split on keyword `com` and take nth value `1`

# Reposts
- [X] Selector `button.ember-view.t-black--light.t-12.hoverable-link-text`
- [X] Keep everything before keyword ` `

# Cleanup todos

- [X] Lower everything and transform i.e. [here](https://www.datacamp.com/tutorial/case-conversion-python) plus dates. etc. Do this last.
- [X] Need to split company followers