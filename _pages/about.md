---
title: "About"
layout: gridlay
sitemap: false
permalink: /about/
---

<h1 class="page-title">About</h1>

{% for member in site.data.pi %}
<div class="jumbotron profile-card" markdown="0">
  <img src="{{ site.url }}{{ site.baseurl }}/images/{{ member.photo }}" alt="{{ member.name }}">
  <div>
    <h3>{{ member.name }}</h3>
    <div class="profile-info">{{ member.info }}{% if member.location %} · {{ member.location }}{% endif %}</div>
    {% include profile_links.html member=member %}
  </div>
</div>

<div class="jumbotron" markdown="0">
  <h3 class="section-title"><i class="fa fa-graduation-cap"></i> Education</h3>
  <ul class="timeline">
    {% for education in member.education %}
      {% assign edu_date = education | split: ")" | first | remove: "(" %}
      {% assign edu_text = education | remove_first: "(" | remove_first: edu_date | remove_first: ")" | strip %}
      <li><span class="tl-date">{{ edu_date | replace: "-", "–" }}</span><span class="tl-text">{{ edu_text }}</span></li>
    {% endfor %}
  </ul>
</div>
{% endfor %}

{% comment %} Grants and awards are stored as "YEAR, text [role]"; split them for the timeline {% endcomment %}
{% if site.data.grants %}
<div class="jumbotron" markdown="0">
  <h3 class="section-title"><i class="fa fa-flask"></i> Grants</h3>
  <ul class="timeline">
    {% for grant in site.data.grants %}
      {% assign g_date = grant.name | split: ", " | first %}
      {% assign g_rest = grant.name | remove_first: g_date | remove_first: ", " | strip %}
      {% assign g_text = g_rest | split: " [" | first %}
      {% assign g_role = "" %}
      {% if g_rest contains " [" %}{% assign g_role = g_rest | split: " [" | last | remove: "]" %}{% endif %}
      <li><span class="tl-date">{{ g_date | replace: "-", "–" }}</span><span class="tl-text">{{ g_text }}{% if g_role != "" %} <span class="tl-tag">{{ g_role }}</span>{% endif %}</span></li>
    {% endfor %}
  </ul>
</div>
{% endif %}

{% if site.data.awards %}
<div class="jumbotron" markdown="0">
  <h3 class="section-title"><i class="fa fa-trophy"></i> Awards</h3>
  <ul class="timeline">
    {% for award in site.data.awards %}
      {% assign a_date = award.name | split: ", " | first %}
      {% assign a_text = award.name | remove_first: a_date | remove_first: ", " | strip %}
      <li><span class="tl-date">{{ a_date }}</span><span class="tl-text">{{ a_text }}</span></li>
    {% endfor %}
  </ul>
</div>
{% endif %}

{% if site.data.peer_reviews %}
<div class="jumbotron" markdown="0">
  <h3 class="section-title"><i class="fa fa-pencil-square-o"></i> Peer review</h3>
  <ul class="timeline">
    {% for peer_review in site.data.peer_reviews %}
      <li><span class="tl-date">{{ peer_review.year }}</span><span class="tl-text">{{ peer_review.role }}, {{ peer_review.name | remove_first: "Journal, " }}</span></li>
    {% endfor %}
  </ul>
</div>
{% endif %}

{% if site.data.people %}
<div class="jumbotron" markdown="0">
  <h3 class="section-title"><i class="fa fa-users"></i> Students and mentoring</h3>
  <ul class="timeline">
    {% for student in site.data.people %}
      <li><span class="tl-date">{{ student.year }}</span><span class="tl-text">{{ student.name }}, {{ student.degree }}, {{ student.location }}</span></li>
    {% endfor %}
  </ul>
</div>
{% endif %}
