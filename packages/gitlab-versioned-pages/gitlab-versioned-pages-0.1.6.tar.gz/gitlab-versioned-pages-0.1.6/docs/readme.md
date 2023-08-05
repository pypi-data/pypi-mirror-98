# gitlab-versioned-pages

[![conda](https://img.shields.io/conda/dn/ostrokach-forge/gitlab-versioned-pages.svg)](https://anaconda.org/ostrokach-forge/gitlab-versioned-pages/)
[![docs](https://img.shields.io/badge/docs-v0.1.6-blue.svg)](https://ostrokach.gitlab.io/gitlab-versioned-pages/v0.1.6/)
[![pipeline status](https://gitlab.com/ostrokach/gitlab-versioned-pages/badges/v0.1.6/pipeline.svg)](https://gitlab.com/ostrokach/gitlab-versioned-pages/commits/v0.1.6/)
[![coverage report](https://gitlab.com/ostrokach/gitlab-versioned-pages/badges/v0.1.6/coverage.svg?job=docs)](https://ostrokach.gitlab.io/gitlab-versioned-pages/v0.1.6/htmlcov/)

Include documentation for multiple project versions in a single GitLab page.

## Overview

This package can be used inside a `pages` job in your `.gitlab-ci.yml` pipeline in order to combine documentation for all tagged versions of the package. See the [`.gitlab-ci.yml`](./.gitlab-ci.yml) of this package for an example.

This package also generates a `versions.json`, which can be used together with e.g. the Sphinx [`msmb_theme`](https://github.com/msmbuilder/msmb_theme) in order to include a version selector on the documentation page for each version

## Usage

Add the following stage in your `.gitlab-ci.yml` file to collect documentations for all tagged versions and include them in a single page. The `GITLAB_TOKEN` is a private token that can be created manually inside the GitLab settings page.

```yaml
pages:
  stage: custom
  before_script:
    - pip install gitlab_versioned_pages
  script:
    - mkdir -p ./public
    - python -m gitlab_versioned_pages
      --project-id ${CI_PROJECT_ID}
      --job-name docs
      --private-token ${GITLAB_TOKEN}
      --output-dir ./public
      --url "https://${CI_PROJECT_NAMESPACE}.gitlab.io/${CI_PROJECT_NAME}"
  artifacts:
    paths:
      - public
  only:
    variables:
      - $UPDATE_PAGES
```

## Implementation details

This file creates a `./public` folder containing documentation created for multiple versions (tags) of this repository.

When the repository is public, our job is easy: we simply download the `artifact.zip` file from a publicly-accessible URL (see: [downloading the latest artifacts]). However, when the repository is private, using the above-mentioned URL does not work (see: [gitlab-org/gitlab-ce#22957]). In that case, we resort to using the GitLab API instead.

If [gitlab-org/gitlab-ce#22957] is ever fixed, we would be able to specify
`--header "Private-Token: XXXXX"` or attach `&private_token=XXXXX` to the query string,
and keep using the original URL:

```bash
curl --header "Private-Token: XXXXX" \
    "https://gitlab.com/user/repo/-/jobs/artifacts/ref/download?job=job_name"
```

Good resource: <https://docs.gitlab.com/ee/api/jobs.html#download-the-artifacts-archive>.

<!-- Links -->

[downloading the latest artifacts]: https://docs.gitlab.com/ee/user/project/pipelines/job_artifacts.html#downloading-the-latest-artifacts
[gitlab-org/gitlab-ce#22957]: https://gitlab.com/gitlab-org/gitlab-ce/issues/22957
