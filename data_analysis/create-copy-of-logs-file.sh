BASE_PATH="/mnt/c/Users/Muhammad Andre G/Downloads/Kuliah stuff/Kuliah/SKRIPSI/Exploration Phase/thesis"
SCENARIO=$1
VERSION=$2
DEST=$BASE_PATH/data-analysis/$SCENARIO/$VERSION

case $1 in
  "only local")
    cp $BASE_PATH/logs/log_MyFrameProducerSc2_4.csv $DEST
    cp $BASE_PATH/logs/log_MyJetsonSc2.csv $DEST
    cp $BASE_PATH/client/logs/log_MyClient.csv $DEST
  ;;

  *)
    echo "unknown scenario"
  ;;
esac
