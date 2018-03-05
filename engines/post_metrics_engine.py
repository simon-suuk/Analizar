class PostMetricsEngine:
    def __init__(self, **kwargs):
        self.total_fan_base = kwargs.get("fan_base")  # Total Page Followers
        self.total_page_fan_adds = kwargs.get("fan_adds")  # daily new likes
        self.total_post_reach = kwargs.get("lifetime_post_reach")
        self.total_post_engagement = kwargs.get("lifetime_engaged_users")
        self.total_number_of_likes = kwargs.get("likes")
        self.total_number_of_shares = kwargs.get("shares")
        self.total_number_of_comments = kwargs.get("comments")
        self.total_number_of_clicks = kwargs.get("clicks")
        self.total_negative_feedback = kwargs.get("lifetime_negative_feedback")

    def get_total_fan_base(self):
        return self.total_fan_base

    def get_total_post_reach(self):
        return self.total_post_reach

    def get_total_post_engagement(self):
        return self.total_post_engagement

    def get_total_number_of_likes(self):
        return self.total_number_of_likes

    def get_total_number_of_shares(self):
        return self.total_number_of_shares

    def get_total_number_of_comments(self):
        return self.total_number_of_comments

    def get_total_number_of_clicks(self):
        return self.total_number_of_clicks

    def get_total_negative_feedback(self):
        return self.total_negative_feedback

    def pct_of_total_post_reach(self):
        if self.total_post_reach == 0 or self.total_fan_base == 0:
            return 0
        pct = 100 * (self.total_post_reach / self.total_fan_base)
        return int(round(pct))

    def pct_of_post_engagement(self):
        if self.total_post_engagement == 0 or self.total_post_reach == 0:
            return 0
        pct = 100 * (self.total_post_engagement / self.total_post_reach)
        return int(round(pct))

    def pct_of_post_negative_feedback(self):
        if self.total_negative_feedback == 0 or self.total_post_engagement == 0:
            return 0
        pct = 100 * (self.total_negative_feedback / self.total_post_engagement)
        return int(round(pct))

        # @staticmethod
        # def pct_of_post_organic_impression(lifetime_post_organic_impression, total_fan_base):
        #     pct = 100 * (lifetime_post_organic_impression / total_fan_base)
        #     return int(round(pct))
        #
        # @staticmethod
        # def pct_of_post_paid_impression(lifetime_post_paid_impression, total_fan_base):
        #     pct = 100 * (lifetime_post_paid_impression / total_fan_base)
        #     return int(round(pct))
        #
        # @staticmethod
        # def pct_of_total_post_impression(lifetime_post_impression, total_fan_base):
        #     pct = 100 * (lifetime_post_impression / total_fan_base)
        #     return int(round(pct))
        #
        # @staticmethod
        # def pct_of_unique_users_on_post(lifetime_post_total_reach, total_fan_base):
        #     pct = 100 * (lifetime_post_total_reach / total_fan_base)
        #     return int(round(pct))
        #
        # # comparing the engagement of one post against another
        # @staticmethod
        # def pct_of_post_engagement(lifetime_engaged_users, lifetime_post_reached):
        #     pct = 100 * (lifetime_engaged_users / lifetime_post_reached)
        #     return int(round(pct))
        #
        # @staticmethod
        # def pct_of_post_impression_effect_on_fan_base(lifetime_post_impression_by_people_who_liked_page, total_fan_base):
        #     pct = 100 * (lifetime_post_impression_by_people_who_liked_page / total_fan_base)
        #     return int(round(pct))
        #
        # @staticmethod
        # def pct_of_post_engagement_effect_on_page(lifetime_people_who_liked_page_and_engaged_post, total_fan_base):
        #     pct = 100 * (lifetime_people_who_liked_page_and_engaged_post / total_fan_base)
        #     return int(round(pct))
        #
        # @staticmethod
        # def pct_of_post_ads_effect_on_page(lifetime_post_paid_impression_by_people_who_liked_page, total_fan_base):
        #     pct = 100 * (lifetime_post_paid_impression_by_people_who_liked_page / total_fan_base)
        #     return int(round(pct))
        #
        # @staticmethod
        # def pct_of_post_content_type_effect_on_page(lifetime_post_reach_by_people_who_liked_page, total_fan_base):
        #     pct = 100 * (lifetime_post_reach_by_people_who_liked_page / total_fan_base)
        #     return int(round(pct))
        #
        # @staticmethod
        # def pct_of_post_negative_feedback(lifetime_negative_feedback_from_users, lifetime_engaged_users):
        #     pct = 100 * (lifetime_negative_feedback_from_users / lifetime_engaged_users)
        #     return int(round(pct))
        #
        # @staticmethod
        # def pct_effect_of_video_without_ads(lifetime_organic_video_views, total_fan_base):
        #     pct = 100 * (lifetime_organic_video_views / total_fan_base)
        #     return int(round(pct))
        #
        # @staticmethod
        # def pct_effect_of_video_with_ads(lifetime_paid_video_views, total_fan_base):
        #     pct = 100 * (lifetime_paid_video_views / total_fan_base)
        #     return int(round(pct))
