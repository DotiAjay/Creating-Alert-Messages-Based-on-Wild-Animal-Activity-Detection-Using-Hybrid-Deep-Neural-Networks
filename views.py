from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,predict_animal_activity_detection,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def index(request):
    return render(request, 'RUser/index.html')

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city,address=address,gender=gender)

        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html',{'object':obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Detect_Animal_Activity_Type(request):
    if request.method == "POST":

        if request.method == "POST":

            Fid= request.POST.get('Fid')
            Forest_Name= request.POST.get('Forest_Name')
            Location= request.POST.get('Location')
            Animal= request.POST.get('Animal')
            Height_cm= request.POST.get('Height_cm')
            Weight_kg= request.POST.get('Weight_kg')
            Color= request.POST.get('Color')
            Diet= request.POST.get('Diet')
            Habitat= request.POST.get('Habitat')
            Predators= request.POST.get('Predators')
            Countries_Found= request.POST.get('Countries_Found')
            Conservation_Status= request.POST.get('Conservation_Status')
            Family= request.POST.get('Family')
            Social_Structure= request.POST.get('Social_Structure')
            Alert_Message_Date= request.POST.get('Alert_Message_Date')

        df = pd.read_csv('Datasets.csv',encoding='latin-1')

        def apply_response(Label):
            if (Label == 0):
                return 0  # crossing the forest lines
            elif (Label == 1):
                return 1  # hindrance to villagers and  tourists people
            elif (Label == 2):
                return 2  # detection of trespassing

        df['Results'] = df['Label'].apply(apply_response)


        X = df['Fid']
        y = df['Results']

        print("RID")
        print(X)
        print("Results")
        print(y)

        cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))
        X = cv.fit_transform(X)



        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Convolutional Neural Network (CNN)")

        from sklearn.neural_network import MLPClassifier
        mlpc = MLPClassifier().fit(X_train, y_train)
        y_pred = mlpc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('MLPClassifier', mlpc))


        # SVM Model
        print("SVM")
        from sklearn import svm

        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print("ACCURACY")
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression

        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))

        print("Decision Tree Classifier")
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtcpredict = dtc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, dtcpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, dtcpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, dtcpredict))
        models.append(('DecisionTreeClassifier', dtc))


        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if (prediction == 0):
            val = 'crossing the forest lines'
        elif (prediction == 1):
            val = 'hindrance to villagers and  tourists people'
        elif (prediction == 2):
            val = 'detection of trespassing'


        print(val)
        print(pred1)

        predict_animal_activity_detection.objects.create(
        Fid=Fid,
        Forest_Name=Forest_Name,
        Location=Location,
        Animal=Animal,
        Height_cm=Height_cm,
        Weight_kg=Weight_kg,
        Color=Color,
        Diet=Diet,
        Habitat=Habitat,
        Predators=Predators,
        Countries_Found=Countries_Found,
        Conservation_Status=Conservation_Status,
        Family=Family,
        Social_Structure=Social_Structure,
        Alert_Message_Date=Alert_Message_Date,
        Prediction=val)

        return render(request, 'RUser/Detect_Animal_Activity_Type.html',{'objs': val})
    return render(request, 'RUser/Detect_Animal_Activity_Type.html')



