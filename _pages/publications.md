---
title: "Publications"
layout: gridlay
sitemap: false
permalink: /publications/
---

<h1 class="page-title">Publications</h1>
<p class="page-lead">Journal articles, patents and conference contributions. My name is highlighted; journal covers open full size.</p>

<div class="jumbotron" markdown="0">
{% include scholar_stats.html %}
</div>

<div class="chips" markdown="0">
  <a class="chip" href="#articles">Journal articles</a>
  <a class="chip" href="#patents">Patents</a>
  <a class="chip" href="#proceedings">Conference proceedings</a>
</div>

{% comment %} Preprints only appear once ref.bib has an @unpublished entry {% endcomment %}
{% capture preprints %}{% bibliography --query @unpublished %}{% endcapture %}
{% if preprints contains "<li" %}
<div class="jumbotron" markdown="0">
<h3 class="section-title" id="preprints">Preprints <span class="count-badge">{% bibliography_count --query @unpublished %}</span></h3>
{{ preprints }}
</div>
{% endif %}

<div class="jumbotron" markdown="0">
<h3 class="section-title" id="articles">Refereed journal articles <span class="count-badge">{% bibliography_count --query @article %}</span></h3>
{% bibliography --query @article %}
</div>

<div class="jumbotron" markdown="0">
<h3 class="section-title" id="patents">Patents <span class="count-badge">{% bibliography_count --query @misc %}</span></h3>
{% bibliography --query @misc %}
</div>

<div class="jumbotron" markdown="0">
<h3 class="section-title" id="proceedings">Refereed conference proceedings <span class="count-badge">{% bibliography_count --query @inproceedings %}</span></h3>
{% bibliography --query @inproceedings %}
</div>

<!-- Dimensions citation badges (one script for every badge on the page) -->
<script async src="https://badge.dimensions.ai/badge.js" charset="utf-8"></script>
