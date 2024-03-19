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
- [ ] Selector: `div.update-components-actor span.update-components-actor__name span.visually-hidden`

# Author Title
- [ ] Selector: `div.update-components-actor span.update-components-actor__description span.visually-hidden`
- [ ] Replace Regex with Value: `/\d+\,*\d+\Wfollowers/gm`

# Author/Company Profile URL
- [ ] Extract URL from `div.update-components-actor.display-flex.update-components-actor--with-control-menu div.update-components-actor__container > a`
- [ ] Split on keyword `?` and take nth value of `1`

# Company Followers
- [ ] Selector `div.update-components-actor span.update-components-actor__description span.visually-hidden`
- [ ] Replace regex `/(^\D*)/gm` with value ``
- [ ] Keep everything before keyword `followers`

# Post Text
- [ ] Selector `span.break-words span`

# Post Likes
- [ ] Selector `.social-details-social-counts__item.social-details-social-counts__reactions.social-details-social-counts__reactions--left-aligned`
- [ ] Split on keyword ` ` and take nth value `1`

# Comments
- [ ] Selector `li.social-details-social-counts__item.social-details-social-counts__comments`
- Split on keyword `com` and take nth value `1`

# Reposts
- [ ] Selector `button.ember-view.t-black--light.t-12.hoverable-link-text`
- [ ] Keep everything before keyword ` `

# Cleanup todos

- [ ] Lower everything and transform i.e. [here](https://www.datacamp.com/tutorial/case-conversion-python)