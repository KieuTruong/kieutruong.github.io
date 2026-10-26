---
title: "News"
layout: textlay
sitemap: false
permalink: /allnews.html
---

<h1 class="page-title">News</h1>

<div class="jumbotron" markdown="0">
<ul class="timeline">
{% for article in site.data.news %}
  <li><span class="tl-date">{{ article.date }}</span><span class="tl-text">{{ article.headline }}</span></li>
{% endfor %}
</ul>
</div>
