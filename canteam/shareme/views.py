from django.shortcuts import render, redirect
from .models import User42, Product, Action, Sponsor
from django.http import HttpResponse
import random

# def pick_a_color():
# 	colors = ["alert-primary", ""]

def select_color_by_coal(coal):
	if coal == "R":
		return "#c0392b"
	if coal == "P":
		return "#9b59b6"
	if coal == "B":
		return "#2980b9"
	if coal == "G":
		return "#27ae60"
	if coal == "Y":
		return "#f1c40f"
	if coal == "O":
		return "#d35400"
	else:
		return "table-secondary"


def update_balance(u):
	purchases = Action.objects.filter(is_order=True, user42=u)
	u.balance = 0
	for p in purchases:
		u.balance -= (p.total - p.paid)
	u.save()

def save_pwd(request):
	if request.method == 'POST':
		u = User42.objects.filter(name = request.POST['u_name']).first()
		if u:
			u.pwd = request.POST['pwd']
			u.save()
		return redirect('42_index', u.name)
	return redirect('home')

def check_or_choose_coal(u_name):
	u = User42.objects.filter(name = u_name).first()
	lista = ["R", "P", "B", "G", "Y", "O"]
	if not u or not u.color:
		return random.choice(lista)
	else:
		return u.color

def check_or_choose_icon(u_name):
	u = User42.objects.filter(name = u_name).first()
	lista = [
		'<i class="bi bi-airplane"></i>', 
		'<i class="bi bi-balloon"></i>', 
		'<i class="bi bi-bicycle"></i>',
		'<i class="bi bi-bug"></i>', 
		'<i class="bi bi-camera"></i>', 
		'<i class="bi bi-cassette">',
		'<i class="bi bi-cloud-drizzle"></i>'
		]
	if not u or not u.icon:
		return random.choice(lista)
	else:
		icon = u.icon.split('<i')[1].split('</i>')[0]
		return f"<i{icon}</i>"

def home(request):
	context = {}
	if request.method == 'POST':
		u_name = request.POST['user42'].lower().strip()
		coal = request.POST['coal']
		if coal == 'none':
			coal = check_or_choose_coal(u_name)
			print(coal)
		icon = request.POST['icon']
		if icon == 'none':
			icon = check_or_choose_icon(u_name)
			print(icon)
		u = User42.objects.filter(name = u_name).first()
		if not u:
			u = User42.objects.create(name=u_name)
		context['user'] = u.name
		u.coalition = coal
		u.color = coal
		# u.color = select_color_by_coal(coal)
		u.icon = f'<b style="color: {select_color_by_coal(coal)}; font-size: 14pt">{icon}</b>'
		u.save()
		if not u.pwd:
			return render(request, 'share42/set_pwd.html', context=context)
		update_balance(u)
		return redirect('42_index', u.name)
	return render(request, 'share42/home.html', context=context)

def index(request, username):
	context = {}
	u = User42.objects.filter(name=username).first()
	context['u'] = u
	if request.method == 'POST':
		if request.POST['mode'] == 'rec':
			return redirect('receivables', u.pk)
		else:
			return redirect("top_up", u.pk)
	context['us'] = User42.objects.all().order_by("-coffee_score")
	return render(request, 'share42/index.html', context=context)

def receivables(request, username):
	u = User42.objects.filter(name=username).first()
	if request.method == 'POST':
		amount = request.POST['amount']
		payer = User42.objects.filter(name=request.POST['u_name']).first()
		if not amount:
			amount = 0
		amount = float(amount)
		acs = Action.objects.filter(product__sponsor__user42=u, is_order=True, user42=payer)
		for ac in acs:
			debt = ac.total - ac.paid
			if amount > 0 and amount <= debt:
				print(f'amount {amount} is smaller than debt {debt}')
				ac.paid += amount
				amount = 0
				ac.save()
			elif amount > 0:
				print(f'amount {amount} is greater than debt {debt}')
				ac.paid = ac.total
				amount -= (ac.total - ac.paid)
				ac.save()
			if amount <= 0:
				break
	context = {}
	acs = Action.objects.filter(product__sponsor__user42=u, is_order=True)
	rs = User42.objects.all()
	for r in rs:
		r.debt = 0
	for ac in acs:
		for r in rs:
			if r == ac.user42 and ac.total - ac.paid != 0:
				r.debt += (ac.total - ac.paid)
	context['rs'] = rs
	context['u'] = u
	return render(request, 'share42/receivables.html', context=context)

def add_prod(request, username):
	context = {}
	u = User42.objects.filter(name=username).first()
	context['u'] = u
	if request.method == 'POST':
		s = Sponsor.objects.filter(user42=u).first()
		if not s:
			s = Sponsor.objects.create(user42=u)
		s.phone = request.POST['phone']
		u.phone = s.phone
		u.save()
		p = Product.objects.create(
			name = request.POST['product'],
			price = request.POST['price_per_unit'],
			unit = request.POST['unit'],
			color = request.POST['color'],
			sponsor = s
		)
		s.save()
		return redirect('42_index', u.name)
	return render(request, 'share42/add_prod.html', context=context)

def prod_cat(request, username):
	context = {}
	context['u'] = User42.objects.filter(name=username).first()
	context['ps'] = Product.objects.filter(active=True)
	return render(request, 'share42/prod_cat.html', context=context)

def top_up(request, username):
	u = User42.objects.filter(name=username).first()
	context = {}
	purchases = Action.objects.filter(is_order=True, user42=u)
	sps = Sponsor.objects.all()
	for s in sps:
		s.total = 0
	for p in purchases:
		for s in sps:
			if s.user42.name == p.product.sponsor.user42.name:
				s.total += (p.total - p.paid)
	context['sponsors'] = sps
	context['u'] = u
	return render(request, 'share42/top_up.html', context=context)

def purchase(request, prod_pk, username):
	u = User42.objects.filter(name=username).first()
	if request.method == 'POST':
		p = Product.objects.get(pk=prod_pk)
		qnt = int(request.POST['qnt'])
		u.balance -= p.price * qnt
		u.coffee_score += qnt
		u.save()
		if u != p.sponsor.user42:
			Action.objects.create(
				user42 = u,
				product = p,
				scoops = qnt,
				total = p.price * qnt,
				balance = u.balance,
				is_order = True
			)
		return redirect("42_index", u.name)
	context = {}
	context['u'] = u
	context['p'] = Product.objects.get(pk=prod_pk)
	return render(request, 'share42/purchase.html', context=context)
