# from flask import Flask, redirect, url_for, jsonify, render_template, make_response, json, send_from_directory
# from flask_dance.contrib.github import make_github_blueprint, github
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from werkzeug.middleware.proxy_fix import ProxyFix
# from pandas import pandas, json_normalize
# from time import sleep, time

# # app = Flask(__name__, static_folder="static")
# # app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
# # app.secret_key = ""
# blueprint = make_github_blueprint(
#     client_id="",
#     client_secret="",
# )
# app.register_blueprint(blueprint, url_prefix="/login")

# @app.route("/")
# def index(name=None):
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     resp = github.get("/user")
#     assert resp.ok
#     user = resp.json()

#     resp = github.get("/rate_limit")
#     assert resp.ok
#     rate = resp.json()
    
#     return render_template('index.html', name=user["login"], rate=rate['resources'])
#     # return "You are @{login} on GitHub".format(login=resp.json()["login"])

# @app.route("/api/user")
# def user():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     resp = github.get("/user")
#     assert resp.ok
#     return resp.json()

# @app.route("/api/repositories")
# def repositories():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     resp = github.get("/search/repositories?per_page=100&q=archived:true+is:public+stars:>=250")
#     assert resp.ok
#     return resp.json()

# @app.route("/api/commits")
# def commits():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     resp = github.get("/search/commits?per_page=100&q=repo:reddit-archive/reddit+author-date:<2020-04-20", headers={"Accept" : "application/vnd.github.cloak-preview"})
#     assert resp.ok
#     return resp.json()

# @app.route("/api/issues")
# def issues():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     resp = github.get("/search/issues?per_page=100&q=repo:reddit-archive/reddit+created:<2020-04-20")
#     assert resp.ok
#     return resp.json()
    
# @app.route("/api/csv/user")
# def userCvs():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     response = github.get("/user")
#     data = response.json()
#     df = json_normalize(data)
    
#     resp = make_response(df.to_csv())
#     resp.headers["Content-Disposition"] = "attachment; filename=user.csv"
#     resp.headers["Content-Type"] = "text/csv"
#     resp.headers["Content-Encoding"] = "utf-8"
#     return resp

# @app.route("/api/csv/repositories")
# def repositoriesCvs():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     response = github.get("/search/repositories?per_page=100&q=archived:true+is:public+stars:>=250")
#     data = response.json()["items"]
#     df = json_normalize(data)
    
#     resp = make_response(df.to_csv())
#     resp.headers["Content-Disposition"] = "attachment; filename=repositories.csv"
#     resp.headers["Content-Type"] = "text/csv"
#     resp.headers["Content-Encoding"] = "utf-8"
#     return resp

# @app.route("/api/repository/commits")
# def repositoryCommits():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     response = github.get("/search/repositories?per_page=100&q=archived:true+is:public+stars:>=250")
#     repository = response.json()["items"][10]
#     repoName = repository["full_name"]
#     query = "/search/commits?per_page=100&q=repo:{repoName}+author-date:<2020-04-20".format(repoName=repoName)
#     resp = github.get(query, headers={"Accept" : "application/vnd.github.cloak-preview"})
#     assert resp.ok
#     commits = resp.json()["items"]
#     analyzer = SentimentIntensityAnalyzer()
#     avgNegRepo = 0
#     avgPosRepo = 0
#     avgNeuRepo = 0
#     avgCompoundRepo = 0
#     nrOfSentences = 0
#     for commit in commits:
#         # Get the message
#         message = commit["commit"]["message"]
#         # replace newline with punctuation
#         message = message.replace("\n", " ").replace("\r", "")
#         # Split the message into sentences
#         sentences = message.split(". ")
#         # Initiate avg vars
#         avgNeg = 0
#         avgPos = 0
#         avgNeu = 0
#         avgCompound = 0
#         for sentence in sentences:
#             # Analyse each sentence
#             vs = analyzer.polarity_scores(sentence)
#             # Sum of all the sentence scores in the message
#             avgCompound += vs['compound']
#             avgNeg += vs['neg']
#             avgPos += vs['pos']
#             avgNeu += vs['neu']
#             nrOfSentences += 1
#             # print("{:-<65} {}".format(sentence, str(vs)))
#         # Divide by number of sentences in message to get average score
#         avgCompound = avgCompound / len(sentences)
#         avgNeg = avgNeg / len(sentences)
#         avgPos = avgPos / len(sentences)
#         avgNeu = avgNeu / len(sentences)

#         # Sum the average of messages
#         avgCompoundRepo += avgCompound
#         avgNegRepo += avgNeg
#         avgPosRepo += avgPos
#         avgNeuRepo += avgNeu

#     # Divide by number of commits to get average for whole repo
#     avgCompoundRepo = avgCompoundRepo / len(commits)
#     avgNegRepo = avgNegRepo / len(commits)
#     avgPosRepo = avgPosRepo / len(commits)
#     avgNeuRepo = avgNeuRepo / len(commits)
#     print("Average compound: {compound} \nAverage negative: {negative}\nAverage positive: {positive}\nAverage neutral: {neutral}".format(compound=avgCompoundRepo, negative=avgNegRepo, positive=avgPosRepo, neutral=avgNeuRepo))

#     # Add values back to json
#     repository['average_compound'] = avgCompoundRepo
#     repository['average_negative'] = avgNegRepo
#     repository['average_positive'] = avgPosRepo
#     repository['average_neutral'] = avgNeuRepo
#     repository['nr_of_commits'] = len(commits)
#     repository['nr_of_sentences'] = nrOfSentences

#     df = json_normalize(repository)
    
#     resp = make_response(df.to_csv())
#     resp.headers["Content-Disposition"] = "attachment; filename=repository.csv"
#     resp.headers["Content-Type"] = "text/csv"
#     resp.headers["Content-Encoding"] = "utf-8"

#     return resp

# @app.route("/api/repositories/commits")
# def repositoriesCommits():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     def getRepositories(page="1", perPage="100", query=None):
#         while True:
#             searchRemaining = getRateLimit()
#             if searchRemaining == 30:
#                break
#             else:
#                 sleep(30)
#         resp = github.get("/search/repositories?page={page}&per_page={perPage}&q={query}".format(page=page, perPage=perPage, query=query))
#         assert resp.ok
#         repositories = resp.json()["items"]
#         totalCount = 0
#         analyzer = SentimentIntensityAnalyzer()
#         # start on 1 because fetching repos is considered as one search request
#         nr = 1
#         for repository in repositories:
#             query = "/search/commits?per_page=100&q=repo:{repoName}+author-date:<2020-04-25".format(repoName=repository["full_name"])
#             response = github.get(query, headers={"Accept" : "application/vnd.github.cloak-preview"})
#             assert response.ok
#             commits = response.json()["items"]
#             avgNegRepo = 0
#             avgPosRepo = 0
#             avgNeuRepo = 0
#             avgCompoundRepo = 0
#             nrOfSentences = 0
#             for commit in commits:
#                 # Get the message
#                 message = commit["commit"]["message"]
#                 # replace newline with punctuation
#                 message = message.replace("\n", " ").replace("\r", "")
#                 # Split the message into sentences
#                 sentences = message.split(". ")
#                 # Initiate avg vars
#                 avgNeg = 0
#                 avgPos = 0
#                 avgNeu = 0
#                 avgCompound = 0
#                 for sentence in sentences:
#                     # Analyse each sentence
#                     vs = analyzer.polarity_scores(sentence)
#                     # Sum of all the sentence scores in the message
#                     avgCompound += vs['compound']
#                     avgNeg += vs['neg']
#                     avgPos += vs['pos']
#                     avgNeu += vs['neu']
#                     nrOfSentences += 1
#                     # print("{:-<65} {}".format(sentence, str(vs)))
#                 # Divide by number of sentences in message to get average score
#                 avgCompound = avgCompound / len(sentences)
#                 avgNeg = avgNeg / len(sentences)
#                 avgPos = avgPos / len(sentences)
#                 avgNeu = avgNeu / len(sentences)

#                 # Sum the average of messages
#                 avgCompoundRepo += avgCompound
#                 avgNegRepo += avgNeg
#                 avgPosRepo += avgPos
#                 avgNeuRepo += avgNeu

#             # Divide by number of commits to get average for whole repo
#             avgCompoundRepo = avgCompoundRepo / len(commits)
#             avgNegRepo = avgNegRepo / len(commits)
#             avgPosRepo = avgPosRepo / len(commits)
#             avgNeuRepo = avgNeuRepo / len(commits)
#             print("Average compound: {compound} \nAverage negative: {negative}\nAverage positive: {positive}\nAverage neutral: {neutral}".format(compound=avgCompoundRepo, negative=avgNegRepo, positive=avgPosRepo, neutral=avgNeuRepo))

#             # Add values back to json
#             repository['average_compound'] = avgCompoundRepo
#             repository['average_negative'] = avgNegRepo
#             repository['average_positive'] = avgPosRepo
#             repository['average_neutral'] = avgNeuRepo
#             repository['nr_of_commits'] = len(commits)
#             repository['nr_of_sentences'] = nrOfSentences
            
#             # repeat logic
#             nr += 1
#             totalCount += 1
#             if nr == 30:
#                 while True:
#                     searchRemaining = getRateLimit()
#                     if searchRemaining == 30:
#                         nr = 0
#                         break
#                     else:
#                         sleep(30)
#             print("{index}\t{repoName}".format(index=str(totalCount), repoName=repository["full_name"]))
#         return repositories

#     # Archived repositories
#     #
#     # >= 250 stars
#     # page 1
#     repositories = getRepositories(query="archived:true+is:public+stars:>=250")
#     # page 2
#     repositories += getRepositories(page="2", query="archived:true+is:public+stars:>=250")
#     # page 3
#     repositories += getRepositories(page="3", query="archived:true+is:public+stars:>=250")
#     # page 4
#     repositories += getRepositories(page="4", query="archived:true+is:public+stars:>=250")
#     # page 5
#     repositories += getRepositories(page="5", query="archived:true+is:public+stars:>=250")

#     # Not archived
#     #
#     # >= 250 stars
#     # page 1
#     repositories += getRepositories(query="archived:false+is:public+stars:>=250")
#     # page 2
#     repositories += getRepositories(page="2", query="archived:false+is:public+stars:>=250")
#     # page 3
#     repositories += getRepositories(page="3", query="archived:false+is:public+stars:>=250")
#     # page 4
#     repositories += getRepositories(page="4", query="archived:false+is:public+stars:>=250")
#     # page 5
#     repositories += getRepositories(page="5", query="archived:false+is:public+stars:>=250")

#     # Normalize results (flatten json)
#     df = json_normalize(repositories)
    
#     resp = make_response(df.to_csv())
#     resp.headers["Content-Disposition"] = "attachment; filename=repositories_final.csv"
#     resp.headers["Content-Type"] = "text/csv"
#     resp.headers["Content-Encoding"] = "utf-8"

#     return resp

# @app.route('/files/<path:filename>', methods=['GET', 'POST'])
# def download(filename):    
#     return send_from_directory(directory='static/files', filename=filename, as_attachment=True)

# def getRateLimit():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     resp = github.get("/rate_limit")
#     assert resp.ok
#     data = resp.json()
#     coreRemaining = data["resources"]["core"]["remaining"]
#     searchRemaining = data["resources"]["search"]["remaining"]
#     print("Core requests remaining: {coreRemaining} \nSearch requests remaining: {searchRemaining}".format(coreRemaining=str(coreRemaining), searchRemaining=str(searchRemaining)))
#     return searchRemaining


# @app.route("/api/limit")
# def rateLimit():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     resp = github.get("/rate_limit")
#     assert resp.ok
#     data = resp.json()
#     return data