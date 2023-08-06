---
title: "{{ replace .Name "-" " " | title }}"
description:
date: "{{ .Date }}"
jobDate: 202
work: []
thumbnail: {{ path.Join (replace .File.Dir "portfolio/" "") "thumbnail.jpg" }}
projectUrl:
# testimonial is optional
testimonial:
  name:
  role:
  image:
  text:
---
