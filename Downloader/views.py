from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from json import dumps
from .functions import *
import shutil


def index(request):
    if request.method == "POST":
        singer = request.POST.get('singer')
        count = int(request.POST.get('count'))
        duration = int(request.POST.get('duration'))
        email = request.POST.get('email')
        Download_Songs(singer, count)
        Convert_To_Audio_Trim(singer, count, duration)
        Merge_Audios(singer, count)
        Audio_to_Zip(singer)
        shutil.rmtree('media/Downloader/audios/'+singer, ignore_errors=True)
        shutil.rmtree('media/Downloader/videos/'+singer, ignore_errors=True)
        zip_file_path = 'media/Downloader/zips/'+singer+' Mashup'+'.zip'
        email = EmailMessage(subject=singer.upper()+' Mashup',
                             body='Mashup of '+singer.upper()+'\nTotal Songs : '+str(count)+"\nDuration of Each Song : "+str(duration), to=[email])
        email.attach_file(zip_file_path)
        email.send()
        os.remove(zip_file_path)
        err = "Mashup of "+singer.upper()+" has been successfully sent to the email id"
        Error = {'Message': err}
        DataError = dumps(Error)
        return render(request, 'Downloader/index.html', {"data": DataError})
        # fs = FileSystemStorage()
        # filename = fs.save(dataset.name, dataset)
        # uploaded_file_url = "."+fs.url(filename)
        # try:
        #     calculate(uploaded_file_url, weights, impacts)
        # except ArgumentsError:
        #     err = "Number of Arguments passed must be equal to 4"
        #     fs.delete(filename)
        #     Error = {'Error': err, 'weights': weights,
        #              'impacts': impacts, 'email': email}

        # except FileNotFoundError:
        #     err = "No such file or directory"
        #     fs.delete(filename)
        #     Error = {'Error': err, 'weights': weights,
        #              'impacts': impacts, 'email': email}

        # except ColumnsError:
        #     err = "Input file must contain three or more columns"
        #     fs.delete(filename)
        #     Error = {'Error': err, 'weights': weights,
        #              'impacts': impacts, 'email': email}

        # except TypeError:
        #     err = "All columns except first must contain numeric values only"
        #     fs.delete(filename)
        #     Error = {'Error': err, 'weights': weights,
        #              'impacts': impacts, 'email': email}

        # except EqualityError:
        #     err = "Number of weights, number of Impacts and number of Columns (from 2nd to last columns) must be same"
        #     fs.delete(filename)
        #     Error = {'Error': err, 'weights': weights,
        #              'impacts': impacts, 'email': email}

        # except ImpactsError:
        #     err = "Impacts must be either +ve or -ve and must be separated by ',' (comma)"
        #     fs.delete(filename)
        #     Error = {'Error': err, 'weights': weights,
        #              'impacts': impacts, 'email': email}

        # except ValueError:
        #     err = "Weights must contain numeric values only and must be separated by ',' (comma)"
        #     fs.delete(filename)
        #     Error = {'Error': err, 'weights': weights,
        #              'impacts': impacts, 'email': email}

        # except CommaError:
        #     err = "Impacts and weights must be separated by ',' (comma)"
        #     fs.delete(filename)
        #     Error = {'Error': err, 'weights': weights,
        #              'impacts': impacts, 'email': email}

        # else:
        #     email = EmailMessage(subject='Topsis Score Evaluation',
        #                          body='Topsis Score of Dataset', to=[email])
        #     email.attach_file("media/Result.csv")
        #     # email.send()
        #     fs.delete("Result.csv")
        #     fs.delete(filename)
        #     err = "The Result File has been successfully sent to the email id"
        #     Error = {'Message': err}
        # finally:
        #     DataError = dumps(Error)
        #     return render(request, 'index.html', {"data": DataError})

    return render(request, 'Downloader/index.html')
