PROJECT_DIR=$( dirname $( dirname $( realpath $0 ) ) )

case ${1?"A repo type is required!"} in
    test)
        REPO="testpypi"
        ;;
    prod)
        REPO="pypi"
        ;;
    *)
        echo "Invalid repo type!"
        exit 1
        ;;
esac

twine upload \
    --repository ${REPO} \
    $PROJECT_DIR/dist/*
