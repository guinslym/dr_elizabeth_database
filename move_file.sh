#moves the files
foreach i (`ls -ltr live_tweets| head -n 142`); do; {mv live_tweets/$i /tmp/dr_elizabeth_database/targets}; done
