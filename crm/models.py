from django.db import models


class Campanha(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.name


class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    fone = models.CharField(max_length=25)
    email = models.EmailField()


class Cobranca(models.Model):
    cliente = models.ForeignKey(Cliente)
    boleto = models.CharField(max_length=50)
    pago = models.BooleanField()
    valor = models.CharField(max_length=50)



