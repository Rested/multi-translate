version=$(<VERSION)

git tag "v$version"
git tag "clients/go/v$version"

git push --tags --force