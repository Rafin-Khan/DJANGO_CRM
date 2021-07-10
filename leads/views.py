from django.contrib import messages
from django.db.models.query import QuerySet
from django.http.request import QueryDict
from agents.mixins import OrganiserAndLoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from django.views.generic import FormView, TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView
from.models import Category, Lead,Agent
from .forms import LeadCategoryUpdateForm, LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, CategoryModelForm


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = "landing.html"


# def landing_page(request):
#     return render(request, 'landing.html')

class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user


        # Initial queryset leads for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                oganisation=user.agent.organisation,
                agent__isnull=False
            )

            # Filter for the agent that was logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({

                "unassigned_leads": queryset

            })
        
        return context

# def lead_list(request):
#     leads = Lead.objects.all()
#     context = {
#         "leads": leads
#     }

#     return render(request, 'leads/lead_list.html', context)

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_details.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user


        # Initial queryset leads for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(oganisation=user.agent.organisation)

            # Filter for the agent that was logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

# def lead_detail(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         "lead": lead
#     }
#     return render(request, 'leads/lead_details.html', context)


class LeadCreateView(OrganiserAndLoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        # Send mail
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form)

# def lead_create(request):

#     form = LeadModelForm()

#     if request.method == "POST":
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")

#     context = {
#         "form": form
#     }
#     return render(request, 'leads/lead_create.html', context)


class LeadUpdateView(OrganiserAndLoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    context_object_name = "lead"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user

        # Initial queryset leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

    # def form_valid(self, form):
    #     form.save()
    #     messages.info(self.request, "You have successfully updated this lead")
    #     return super(LeadUpdateView, self).form_valid(form)

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadModelForm(instance=lead)

#     if request.method == "POST":
#         form = LeadModelForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")
            
#     context = {
#         "lead": lead,
#         "form": form
#     }
#     return render(request, 'leads/lead_update.html', context)


class LeadDeleteView(OrganiserAndLoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user

        # Initial queryset leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

# def lead_delete(request, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect("/leads")


# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()

#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect("/leads")
            
#     context = {
#         "lead": lead,
#         "form": form
#     }
#     return render(request, 'leads/lead_update.html', context)


# def lead_create(request):

    # form = LeadForm()

    # if request.method == "POST":
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
#             return redirect("/leads")

#     context = {
#         "form": form
#     }
#     return render(request, 'leads/lead_create.html', context)

class AssignAgentView(OrganiserAndLoginRequiredMixin, FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        # Pass in extra arguments to the form
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                oganisation=user.agent.organisation
            )
        context.update({

            "unassigned_lead_count": queryset.filter(category__isnull=True).count()

        })
        
        return context

    def get_queryset(self):
        user = self.request.user


        # Initial queryset leads for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                oganisation=user.agent.organisation
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, DeleteView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # Context not really needed just understanding
    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     # Get leads queryset from model using the related_names feature.
    #     leads = self.get_object().leads.all()

    #     context.update({

    #         "leads": leads

    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user


        # Initial queryset leads for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                oganisation=user.agent.organisation
            )
        return queryset


class CategoryCreateView(OrganiserAndLoginRequiredMixin, CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)



class CategoryUpdateView(OrganiserAndLoginRequiredMixin, UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user


        # Initial queryset leads for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                oganisation=user.agent.organisation
            )
        return queryset


class CategoryDeleteView(OrganiserAndLoginRequiredMixin, DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user


        # Initial queryset leads for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                oganisation=user.agent.organisation
            )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(oganisation=user.agent.organisation)

            # Filter for the agent that was logged in
            queryset = queryset.filter(agent__user=user)
        return queryset