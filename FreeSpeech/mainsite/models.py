from django.db import models

# Create your models here.
class Mood(models.Model):
    status = models.CharField(max_length=10,null=False)
    def __unicode__(self):
        return self.status
    def __str__(self):
        return self.status

class Post(models.Model):
    mood = models.ForeignKey('Mood',on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10,default='不愿透露身份的人')  #发帖者的昵称
    message = models.TextField(null=False)  #留言内容
    del_pass = models.CharField(max_length=10)  #记录可以删除此篇信息的密码
    pub_time = models.DateTimeField(auto_now=True)  #自动填入的修改时间
    enabled = models.BooleanField(default=False)     #决定是否要把信息显示在网页上
    def __unicode__(self):
        return self.message
    def __str__(self):
        return self.message