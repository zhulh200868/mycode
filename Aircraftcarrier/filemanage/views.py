import datetime,json,sys
import urllib
from .models import FileInfo,ServiceInfo,OperationRecord
from django.http import HttpResponse

# Create your views here.
def newdatas(request):
    try:
        datas=json.loads(request.body)
        files=datas['filelist']
    except Exception as e:
        result={'result':'false','detail':'json error'}
        return HttpResponse(json.dumps(result))

    for i in range(len(files)):
        print files[i]
        try:
            try:
                json_salt_path=str(files[i]['salt_path'])
            except:
                files[i]['result']='false'
                files[i]['detail']='the salt_path is nulll'
                continue

            try:
                json_md5=str(files[i]['md5'])
            except:
                json_md5=''
            s_f=ServiceInfo.objects.filter(service=str(files[i]['service']),cluster_name=str(files[i]['cluster_name']))
            if s_f.exists():
                s_o=ServiceInfo.objects.get(service=str(files[i]['service']),cluster_name=str(files[i]['cluster_name']))
            else:
                s_o=ServiceInfo(service=str(files[i]['service']),
                    cluster_name=str(files[i]['cluster_name']),
                    install_path=str(files[i].get('install_path',''))
                    )
                s_o.save()

            f_o=FileInfo(salt_path=json_salt_path,
                target_path=str(files[i]['target_path']),
                auth=str(files[i]['auth']),
                user_group=str(files[i]['user_group']),
                user=str(files[i]['user']),
                md5=str(files[i].get('md5','')),
                service_info=s_o,
                update_time=datetime.date.today().strftime("%Y%m%d")
                )
            f_o.save()

            o_c=OperationRecord(salt_path=json_salt_path,
                action='insert',
                operate_time=datetime.date.today().strftime("%Y%m%d"),
                file_info_id=f_o.id
                )
            o_c.save()

            files[i]['result']='true'
            files[i]['detail']='inserted'
        except Exception as e:
            files[i]['result']='false'
            files[i]['detail']=str(e)

    result_content={'filelist':files}
    ##return HttpResponse(request.body)
    return HttpResponse(json.dumps(result_content))

def updatedatas(request):
    try:
        datas=json.loads(request.body)
        files=datas['filelist']
    except Exception as e:
        result={'result':'false','detail':'json error'}
        return HttpResponse(json.dumps(result))

    for i in range(len(files)):
        try:
            try:
                json_salt_path=str(files[i]['salt_path'])
            except:
                files[i]['result']='false'
                files[i]['detail']='the salt_path is nulll'
                continue
            try:
                f_g=FileInfo.objects.get(salt_path=json_salt_path)
            except Exception as e:
                files[i]['result']='false'
                files[i]['detail']=str(e)
                continue

            for (key,values) in files[i].items():
                if key in ('service','cluster_name','install_path'):
                    continue
                else:
                    setattr(f_g, key, values)
            setattr(f_g,'update_time',datetime.date.today().strftime("%Y%m%d"))
            f_g.save()
            files[i]['result']='true'
            files[i]['detail']='updated'

            o_c=OperationRecord(salt_path=json_salt_path,
                action='update',
                operate_time=datetime.date.today().strftime("%Y%m%d"),
                file_info_id=f_g.id
                )
            o_c.save()

        except Exception as e:
            files[i]['result']='false'
            files[i]['detail']=str(e)

    result_content={'filelist':files}
    return HttpResponse(json.dumps(result_content))


def downfile(request):
    try:
        datas=json.loads(request.body)
        files=datas['filelist']
    except Exception as e:
        result={'result':'false','detail':'json error'}
        return HttpResponse(json.dumps(result))

    for i in range(len(files)):
        try:
            order_path = ""
            try:
                json_salt_path=str(files[i]['salt_path'])
                order_path = json_salt_path
            except:
                files[i]['result']='false'
                files[i]['detail']='the salt_path is nulll'
                continue
            salt_path_list = json_salt_path.split('/')
            print(salt_path_list)
            print("/".join(salt_path_list))

            success = False
            for k in range(len(salt_path_list)):
                json_salt_path = "/".join(salt_path_list[0:len(salt_path_list)-k])

                f_f=FileInfo.objects.filter(salt_path=json_salt_path)
                if f_f.exists():
                    f_f_detail=f_f.values()[0]
                    try:
                        s_f=ServiceInfo.objects.get(id=f_f_detail['service_info_id'])
                        # s_f.install_path
                    except Exception as e:
                        files[i]['result']='false'
                        files[i]['detail']='the salt_path has no service'
                        continue

                    f_f_detail['service']=s_f.service
                    f_f_detail['cluster_name']=s_f.cluster_name
                    f_f_detail['install_path']=s_f.install_path
                    f_f_detail['target_path']=f_f_detail['target_path']+'/'+('/'.join(salt_path_list[len(salt_path_list)-k:]))
                    f_f_detail['target_path']=f_f_detail['target_path'][:-1]  if f_f_detail['target_path'][len(f_f_detail['target_path'])-1]=='/' else f_f_detail['target_path']
                    f_f_detail['salt_path']=order_path
                    files[i].update(f_f_detail)
                    success = True
                    break
            if not success:
                files[i]['result']='false'
                files[i]['detail']='Can\'t find this salt_path'
            else:
                files[i]['result']='true'
        except Exception as e:
            files[i]['result']='false'
            files[i]['detail']=str(e)
    result_content={'filelist':files}
    ##return HttpResponse(request.body)
    return HttpResponse(json.dumps(result_content))

def downfilebysoft(request):
    try:
        datas=json.loads(request.body)
        json_service=str(datas['service'])
        json_cluster_name=str(datas['cluster_name'])
    except Exception as e:
        result={'result':'false','detail':'json error'}
        return HttpResponse(json.dumps(result))

    result_content={}
    filelist=[]
    try:
        s_g=ServiceInfo.objects.get(service=json_service,cluster_name=json_cluster_name)
        f_f=FileInfo.objects.filter(service_info=s_g)
        filelist.extend(f_f.values())

        result_content['service']=s_g.service
        result_content['cluster_name']=s_g.cluster_name
        result_content['install_path']=s_g.install_path
        result_content['filelist']=filelist
        result_content['result']='true'
    except Exception as e:
        result_content['service']=json_service
        result_content['cluster_name']=json_cluster_name
        result_content['result']='false'
        result_content['detail']=str(e)

    return HttpResponse(json.dumps(result_content))


