class PerformanceInferenceEngine:
    def __init__(self):
        self.__performance = "undefined"

    def get_performance(self):
        return self.__performance

    # Rate: High(80% - 100%), Ok(40% - 79%), Low(0 - 39%)
    def make_inference(self, metric, performance):
        if metric == 'REACH':
            if performance >= 80:
                self.__performance = "high"
                return 'display_suggestion_1_from_knowledge_base'
            elif 40 <= performance < 80:
                self.__performance = "ok"
                return 'display_suggestion_2_from_knowledge_base'
            elif performance < 40:
                self.__performance = "low"
                return 'display_suggestion_3_from_knowledge_base'
        elif metric == 'ENGAGEMENT':
            if performance >= 80:
                self.__performance = "high"
                return 'display_suggestion_1_from_knowledge_base'
            elif 40 <= performance < 80:
                self.__performance = "ok"
                return 'display_suggestion_2_from_knowledge_base'
            elif performance < 40:
                self.__performance = "low"
                return 'display_suggestion_3_from_knowledge_base'
        elif metric == 'PAGE_FOLLOWS':
            if performance >= 80:
                self.__performance = "high"
                return 'display_suggestion_1_from_knowledge_base'
            elif 40 <= performance < 80:
                self.__performance = "ok"
                return 'display_suggestion_2_from_knowledge_base'
            elif performance < 40:
                self.__performance = "low"
                return 'display_suggestion_3_from_knowledge_base'
        elif metric == 'NEGATIVE_FEEDBACK':
            if performance >= 80:
                self.__performance = "high"
                return 'display_suggestion_1_from_knowledge_base'
            elif 40 <= performance < 80:
                self.__performance = "ok"
                return 'display_suggestion_2_from_knowledge_base'
            elif performance < 40:
                self.__performance = "low"
                return 'display_suggestion_3_from_knowledge_base'
        else:
            return 'undefined_metric'
