from splitcli.experiment.experiment import Experiment

def run_experiment(sdk_token, split_name):
	experiment = Experiment(20000, split_name)

	# Support small adjustment to targets to make numbers look natural
	# Support deterministically random defaults for non-significant values
	# Support setting mean and p-value and then choosing smallest arbitrary delta
	experiment.register(experiment.event_result("onboarding_started", {}).probability(0,1,1).count(0,1,1).average(0,1,0))
	experiment.register(experiment.event_result("onboarding_progress", { "stage": "search" }, property_value="elapsed_time").probability(.06,1,.88).count(0, 1, 1).average(.08,.28,35))
	experiment.register(experiment.event_result("onboarding_progress", { "stage": "compare" }, property_value="elapsed_time").probability(-.03,1,.74).count(0, 1, 1).average(-.03,.34,82))
	experiment.register(experiment.event_result("onboarding_progress", { "stage": "plan" }, property_value="elapsed_time").probability(-.01,1,.71).count(0, 1, 1).average(.02,.76,167))
	experiment.register(experiment.event_result("onboarding_progress", { "stage": "report" }, property_value="elapsed_time").probability(-1,1,.46).count(0, 1, 1).average(-1,0,295))
	experiment.register(experiment.event_result("onboarding_completed", {}).probability(.11,1,.46).count(0, 1, 1).average(-.41,.002,300))

	# Return Rate (1, 7, 30 day)
	experiment.register(experiment.event_result("session_start", {}, property_value="user_age").probability(.1043,.043,.45).count(0,1,3).average(0,1,1*86400000+1))
	experiment.register(experiment.event_result("session_start", {}, property_value="user_age").probability(.1442,.021,.32).count(0,1,5).average(0,1,7*86400000+1))
	experiment.register(experiment.event_result("session_start", {}, property_value="user_age").probability(.2187,.0031,.18).count(0,1,2).average(0,1,30*86400000+1))

	# Survey
	experiment.register(experiment.event_result("new_user_survey", {}, property_value="survey_score").probability(.026,.92,.60).count(0, 1,1).average(.9,.0032,62.5))

	# Activity
	experiment.register(experiment.event_result("search", {}).probability(.04,1,.93).count(.03,.8,1).average(0,1,1))
	experiment.register(experiment.event_result("compare", {}).probability(.01,1,.41).count(-.0083,.8,1).average(0,1,1))
	experiment.register(experiment.event_result("plan", {}).probability(.01,1,.23).count(.063,.42,1).average(0,1,1))
	experiment.register(experiment.event_result("report", {}, property_value="load_time").probability(-.20,.87,.375).count(-.26,.017,3).average(-.08,.04,45))
	experiment.register(experiment.event_result("booking", {}).probability(.08,1,.35).count(0,1,1).average(.07,.89,270))

	# Errors
	experiment.register(experiment.event_result("exception", { "platform": "mobile" }).probability(.023,1,.002).count(0.10,.871,0.08).average(0,1,0))
	experiment.register(experiment.event_result("exception", { "platform": "desktop" }).probability(2.041,1,.012).count(1.10,.041,1.5).average(0,1,0))

	experiment.run(sdk_token)

# Onboarding Completion Rate : % of users who complete 
# Onboarding Completion Time
# Onboarding Progress

# Return Rate 1 day
# Return Rate 7 day
# Return Rate 30 day
# Sessions Count

# Survey Completion : % of users who surveyed
# Average Survey Score : Average of new_user_survey

# Purchase Rate : % of users who purchase
# Reports Run : # of Reports Run
# Time to Checkout
# Cancellation Rate
# Errors by Mobile vs Desktop
# Onboarding completion by Region
# Lifetime Value