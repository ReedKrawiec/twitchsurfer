
def generate_streamer_schedule(streamer, twitch_client):
    # Generates a weekly schedule that'll hopefully represent each streamers schedule
    # follow the 3 sd rule when detecting anomalies
    # https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule
    # compute the precise time by finding the median and rounding to the nearest half-hour
    streamer_id = get_user_id(streamer)

    # NOTE: Twitch uses the UTC +0 timezone so we will too 
    local_today = datetime.datetime.now(pytz.timezone(LOCAL_TIMEZONE))
    utc_today = local_today.astimezone(pytz.utc)
    utc_week_start = utc_today - datetime.timedelta(weeks=1)

    FINAL_DATA = []

    # Begin collecting VOD data
    # How many weeks of VOD data to collect
    WEEK_DEPTH = 10
    TOTAL_VODS = 0
    for _ in range(WEEK_DEPTH):
        # TODO: support pagination
        # NOTE: This implementation WILL break without pagination support when processing vods over many weeks
        vods = get_vods(utc_week_start, utc_today, streamer_id)

        # Iterate through all of the vods within the local week and generate a schedule
        # 168 hrs in a week * 2 & sampling 30 minute intervals
        STREAM_STATUS = [0 for j in range(168 * 2)]

        for vod in vods[0]:
            status_index_start = vod['start_time'] - utc_week_start
            #status_index_end = vod['end_time'] - utc_week_start

            status_index_start = int(status_index_start.total_seconds() / 1800)
            #status_index_end = int(status_index_end.total_seconds() / 1800)
            if status_index_start >= 336:
                print("MADE A POOSIE WOOSPIE")
                pdb.set_trace()


            FINAL_DATA.append(status_index_start)
            STREAM_STATUS[status_index_start] = 1
            #for x in range(status_index_start, status_index_end):
            #    STREAM_STATUS[x] = 1


        # Keep track of the vods per week to come up with the number of clustering groups
        # TODO: probably better to use the median instead of the mean
        TOTAL_VODS += len(vods)

        # Plot the vod schedule of a streamer every week
        #plt.plot(STREAM_STATUS)
        #FINAL_DATA.append(STREAM_STATUS)

        # Update these variables per week
        utc_today = utc_week_start
        utc_week_start = utc_week_start - datetime.timedelta(weeks=1)


    
    # (SCRAPED) Begin k-means/medians
    # Kernel Density Estimation models the problem the best
    # https://scikit-learn.org/stable/modules/density.html

    #Flatten FINAL_DATA array
    #FLAT_DATA = []
    #for week in FINAL_DATA:
    #    for vod_time in range(week):
    #        FLAT_DATA.append(vod_time)

    #plot_arr(FINAL_DATA)
    # Pickle file for debugging
    pickle.dump(FINAL_DATA, open("tmp.p", "wb")) 
    # Tweak the bandwith to configure the strictness on what "counts" towards a particular streaming time
    # (remember that 1 unit = 30 minutes)
    # ie. rn, if a user streams on Monday at 11:00 and 12:00, each stream counts towards being part of the schedule
    # however, at 12:30 it does not
    arr_to_kde(FINAL_DATA, debug=True, bandwidth=2, kernel='gaussian', sample_start=0, sample_end=336, sample_num=336)
    plt.show()