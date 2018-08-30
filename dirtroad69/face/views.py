from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .models import Cow, CattleImage, CattleLog
from .forms import UserForm, UserLoginForm, CattleImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import os
from skimage.transform import resize
from PIL import Image
import time
from datetime import timedelta
import numpy as np
from sklearn.externals import joblib
import tensorflow as tf

from django.db.models import Q
from .cfrs import getTransfer1

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
#PATH = 'C:/Users/Reg2017/PycharmProjects/JeffDropsIT/DirtRoad69'
PATH = 'C:/Users/Reg2017/Desktop/final_step/JeffDropsIT/DirtRoad69'
from PIL import Image
#im = Image.open(path)
data_dir = 'C:\\Users\\Reg2017\\PycharmProjects\\JeffDropsIT\\DirtRoad69\\face\\inception' # directory for inception model
path_graph_def = "classify_image_graph_def.pb" # inception model downloaded graph
label = np.array([ [1.,  0.,  0.]])  # label with one-hot encode
graph = tf.Graph()

# Set the new graph as the default.
with graph.as_default():

# TensorFlow graphs are saved to disk as so-called Protocol Buffers
# aka. proto-bufs which is a file-format that works on multiple
# platforms. In this case it is saved as a binary file.

# Open the graph-def file for binary reading.
        path = os.path.join(data_dir, path_graph_def)
        with tf.gfile.FastGFile(path, 'rb') as file:
             # The graph-def is a saved copy of a TensorFlow graph.
             # First we need to create an empty graph-def.
            graph_def = tf.GraphDef()

            # Then we load the proto-buf file into the graph-def.
            graph_def.ParseFromString(file.read())

                # Finally we import the graph-def to the default TensorFlow graph.
            tf.import_graph_def(graph_def, name='')
session = tf.Session(graph=graph)
print("graph created successfully")

def convert_2_1D_array(t_v_i, clf):
    for i in clf.predict(t_v_i):
        i
    return i

def get_index(array):
    count = 0
    for i in array:
        if i == 1:
            count = 0
        else:
            count += 1
    return count

def percentage(transfer_values_im, clf):
    item = np.array(clf.predict_proba(transfer_values_im))
    all_scores = []
    for i in item:
        score = i[0][1]
        all_scores.append(score)
    maximum = max(all_scores)
    return maximum


def useTensor(img):
    #graph, session = getTransfer.graphing()
    #session = getTransfer.tf.Session(graph=graph)
    # In[14]:
    transfer_layer = graph.get_tensor_by_name('pool_3:0')

    transfer_values_im, time_dif = getTransfer1.transfer_values(image=img)

    clf = inception_check_up()
    item = get_index(convert_2_1D_array(transfer_values_im, clf))
    acc = percentage(transfer_values_im, clf)
    x, y_true, y_pred_cls, sess = getTransfer1.restore()

    # In[65]:

    feed_dict = {x: transfer_values_im, y_true: getTransfer1.label}

    # In[66]:

    cls_pred = sess.run(y_pred_cls, feed_dict=feed_dict)


    # In[67]:

    return getTransfer1.getClass(cls_pred), float(acc), item, time_dif

def inception_check_up():
    #joblib.dump(clf, 'C:\\peri\\Decision_tree.pkl')
    clf_decision = joblib.load('C:\\peri_new1\\Decision_tree.pkl')
    print("Successful")
    return clf_decision

def retrain(request):
    if not request.user.is_authenticated():
        return render(request, 'face/login.html')
    else:
        return render(request, 'face/retrain.html')

def class_name(pk_temp):
    if pk_temp == 0:
        pk = 4
    elif pk_temp == 1:
        pk = 2
    elif pk_temp == 2:
        pk = 3
    return pk

def classification(request):
    if not request.user.is_authenticated():
        return render(request, 'face/login.html')
    else:
        form = CattleImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            cattleImage = form.save(commit=False)
            #cattleImage.user = request.user
            cattleImage.classify_img = request.FILES['classify_img']
            file_type = cattleImage.classify_img.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'cattleImage': cattleImage,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'face/classify.html', context)
            cattleImage.save()
            img = CattleImage.objects.last()
            path = PATH + img.classify_img.url

            img = Image.open(path)
            img = img.resize((200, 200), Image.ANTIALIAS)
            #img.get_absolute_url()


            pk_temp, acc, item, time_taken = useTensor(img=img)
            img = CattleImage.objects.last()
            print(pk_temp)
            pk = class_name(pk_temp)
            item = class_name(pk_temp)
            #else:
               # error_message = "There system failed to classify the image provided please use other methods to classify the cow"
                #pk=2
            cow = get_object_or_404(Cow, pk=pk)
            return render(request, 'face/detail.html', {'cow': cow,
                                                        'img': img,
                                                        'acc': '%.1f' % (acc*100),
                                                        'item': get_object_or_404(Cow, pk=item),
                                                        'error_message': 'Uploaded Image',
                                                        'time_taken': str(round(time_taken,2))+str(' sec')

                                                        })
        context = {
            "form": form,
        }
        return render(request, 'face/classify.html', context)





class IndexView(generic.ListView):
    template_name = 'face/index.html'
    login_url = 'face/login.html'
    context_object_name = 'all_cows'

    def get_queryset(self):
        result = Cow.objects.all()

        query = self.request.GET.get('q')
        if query:
            result = result.filter(
                Q(name__icontains=query) |
                Q(breed__icontains=query) |
                Q(gender__icontains=query)
            ).distinct()

        return result


class DetailView(generic.DetailView):
    model = Cow

    template_name = 'face/detail.html'


class CowCreate(CreateView):
    model = CattleLog
    fields = ['log','lactating','feeding_scheme','condition_score', 'injection_type', 'weight', 'injection_Last_Date', 'insemination_date' ]


class CowUpdate(UpdateView):
    model = CattleLog
    fields = ['log','lactating','feeding_scheme','condition_score', 'injection_type', 'weight', 'injection_Last_Date', 'insemination_date' ]


class CowDelete(DeleteView):
    model = Cow
    success_url = reverse_lazy('face:index')


#class ClassifyView(CreateView):
  #  model = CattleImage
  #  login_url = 'face/login.html'
  #  fields = ['classify_img']
   # template_name = 'face/classify.html'

class UserFormView(View):
    form_class = UserForm
    template_name = 'face/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (nomarlized_data)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #authenticate user
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('face:index')
        return render(request, self.template_name, {'form': form})     # try again


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'face/index.html')
            else:
                return render(request, 'face/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'face/login.html', {'error_message': 'Invalid login'})
    return render(request, 'face/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'face/login.html', context)

