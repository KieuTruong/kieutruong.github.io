---
title: "Research"
layout: gridlay
sitemap: false
permalink: /research/
---

<h1 class="page-title">Research</h1>
<p class="page-lead">I design carbon nanostructures and electrocatalysts for energy conversion, storage and light management, from mechanism to scalable synthesis. Click any figure to view it full size.</p>

{% for topic in site.data.research %}
<article class="jumbotron research-card" markdown="0">
  <a href="{{ site.url }}{{ site.baseurl }}/images/{{ topic.image }}" target="_blank"><img src="{{ site.url }}{{ site.baseurl }}/images/{{ topic.image }}" alt="{{ topic.title }}" loading="lazy"></a>
  <div class="research-body">
    <span class="research-tag">{{ topic.tag }}</span>
    <h3>{{ topic.title }}</h3>
    <p>{{ topic.summary }}</p>
    {% if topic.highlights %}
    <ul>
      {% for item in topic.highlights %}<li>{{ item }}</li>{% endfor %}
    </ul>
    {% endif %}
  </div>
</article>
{% endfor %}
