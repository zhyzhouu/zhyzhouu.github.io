# Updating the homepage

Edit index.html for biography, publications and links. academic.css contains the academic layout and overrides styles.css.

## Optional TL;DR

Add a data-tldr attribute to a paper's opening article tag:

```html
<article class="paper" data-tldr="One sentence describing the main takeaway.">
```

Omit the attribute or leave it empty to hide the TL;DR. The first paper includes an editable example.

## Paper figures

Save a figure under assets/ and replace everything inside the paper-thumb link with an image:

```html
<a class="paper-thumb" href="https://arxiv.org/abs/XXXX.XXXXX" target="_blank" rel="noreferrer">
  <img src="assets/paper-name.png" alt="Short description of the paper figure" loading="lazy">
</a>
```

Images are fully visible and keep their original proportions inside a consistent thumbnail area. White space is expected for very wide or tall figures. Expanding Abs or Bib does not resize the thumbnail. Panels are moved into the full-width card row on page load.

## Publishing

Commit the changed files and push to the branch configured in GitHub Settings → Pages. Keep the existing GitHub Pages configuration.
