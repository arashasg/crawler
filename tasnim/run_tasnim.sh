while true; do
    read -p "Run the crawler and remove the previous data? " yn
    case $yn in
        [Yy]* ) rm data/tasnim.csv
                scrapy runspider --set FEED_EXPORT_ENCODING=utf-8 tasnim.py -o data/tasnim.csv ; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

