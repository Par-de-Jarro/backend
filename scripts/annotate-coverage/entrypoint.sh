#!/bin/bash
set -e
set -u
set -o pipefail
set -x

if [[ -z "$GITHUB_TOKEN" ]]; then
	echo "GITHUB_TOKEN should be set."
	exit 1
fi

main() {
    curl -sSL -H  "Accept: application/vnd.github.v3+json" -H "Authorization: token ${GITHUB_TOKEN}" \
    "${GITHUB_API_URL}/repos/${GITHUB_REPOSITORY}/pulls?head=${GITHUB_REPOSITORY_OWNER}:${GITHUB_HEAD_REF}" > pull_request.json

    PR_BASE_SHA=$(jq -r '.[0].base.sha' < pull_request.json)
    PR_HEAD_SHA=$(jq -r '.[0].head.sha' < pull_request.json)

    export PR_BASE_SHA
    export PR_HEAD_SHA

    git fetch origin

    diff_files=$(git diff --name-only --diff-filter=AM "$PR_BASE_SHA" "$PR_HEAD_SHA")
    changed_python_files=$(echo "$diff_files" | grep -E '\.py$' || true)

    if [[ -z "$changed_python_files" ]]; then
        echo "No python files changed, skipping coverage"
    else
        files=$(echo "$changed_python_files" | tr '\n' ' ')
        echo "Running coverage"
        source .venv/bin/activate
        python -m coverage json
        dirname=$(dirname "$0")
        python "$dirname/annotate.py" $files
    fi
}

main "$@"
