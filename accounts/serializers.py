# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from .models import User


# class RegisterSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             "first_name",
#             "last_name",
#             "email",
#             "password",
#             "is_active",
#             "is_staff",
#             "join_date",
#         ]
#         read_only_fields = ["join_date"]

#     def create(self, validated_data):
#         password = validated_data.pop("password")
#         user = User.objects.create_user(password=password, **validated_data)
#         return user


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(
#             email=data["email"],
#             password=data["password"]
#         )

#         if not user:
#           raise serializers.ValidationError("Invalid credentials")

#         return user

#         class UserSerializer(serializers.ModelSerializer):

#             class Meta:

#                 model = User
#                 fields = [
#                     "id",
#                     "first_name",
#                     "last_name",
#                     "email",
#                     "is_active",
#                     "is_staff",
#                     "join_date",
#                 ]  


from rest_framework import serializers  # تصحيح: f صغيرة مو F
from django.contrib.auth import authenticate
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_staff",
            "join_date",
        ]
        read_only_fields = ["join_date"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data["email"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        return user

# لازم يكون الكلاس هون، على الحافة تماماً (بدون أي فراغات قبله)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "join_date",
        ]