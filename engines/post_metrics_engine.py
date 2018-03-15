def pct_of_total_post_reach(lifetime_post_reach, fan_base):
    if lifetime_post_reach == 0 or fan_base == 0:
        return 0
    pct = 100 * (lifetime_post_reach / fan_base)
    return int(round(pct))


def pct_of_post_engagement(lifetime_engaged_users, lifetime_post_reach):
    if lifetime_engaged_users == 0 or lifetime_post_reach == 0:
        return 0
    pct = 100 * (lifetime_engaged_users / lifetime_post_reach)
    return int(round(pct))


def pct_of_post_negative_feedback(lifetime_negative_feedback, lifetime_engaged_users):
    if lifetime_negative_feedback == 0 or lifetime_engaged_users == 0:
        return 0
    pct = 100 * (lifetime_negative_feedback / lifetime_engaged_users)
    return int(round(pct))
