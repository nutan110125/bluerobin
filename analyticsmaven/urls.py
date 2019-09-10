from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url
from analyticsmaven import views


urlpatterns = [
    ############### Employee Register Management URL ###############
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^explore-seekers$', views.LookingForJob.as_view(), name='looking-for-job'),
    url(r'^explore-employers$', views.EmployersList.as_view(), name='employers'),
    ############### Employee Register Management URL ###############
    url(r'^registration$', views.Registration.as_view(), name='registration'),
    url(r'^user-image$', views.UserImage.as_view(), name='user-image'),
    url(r'^chat-attachment$', views.Attachment.as_view(), name='chat-attachment'),
    url(r'^registration-details/(?P<uuid>[0-9a-f-]+)$', views.RegistrationDetails.as_view(), name='registration-details'),
    url(r'^user-skills/(?P<uuid>[0-9a-f-]+)$',views.UserSkill.as_view(), name='user-skills'),
    url(r'^user-details/(?P<uuid>[0-9a-f-]+)$',views.UserDetails.as_view(), name='user-details'),
    url(r'^user-skill-rate$',views.UserSkillRating.as_view(), name='user-skill-rate'),

    ############### Company Register Management URL ###############
    url(r'^company-registration/(?P<uuid>[0-9a-f-]+)$',views.CompanyRegistration.as_view(), name='company-registration'),
    url(r'^industry-type/(?P<uuid>[0-9a-f-]+)$',views.CompanyIndustryType.as_view(), name='industry-type'),

    ############### Profile Activation Management URL ###############
    url(r'^activate-your-account/(?P<uuid>[0-9a-f-]+)$',views.Activate.as_view(), name='activate-your-account'),

    ############### User Management URL ###############
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),
    url(r'^forgot/(?P<uuid>[0-9a-f-]+)$',views.Forgot.as_view(), name='forgot'),
    url(r'^forgotpassword/$',views.ForgotPasswordUser.as_view(), name='forgotpassworduser'),
    url(r'^changepassword$',views.ChangePassword.as_view(), name='changepassword'),
    url(r'^view-profile$',views.ViewProfile.as_view(), name='view-profile'),
    url(r'^edit-profile$',views.EditProfile.as_view(), name='edit-profile'),
    url(r'^reset-password/(?P<uuid>[0-9a-f-]+)$',views.ResetUserPassword.as_view(), name='reset-password'),

    ############### Employee Profile Management URL ###############
    url(r'^dashboard$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^add-education$', views.AddEducation.as_view(), name='education'),
    url(r'^delete-education/(?P<pk>[0-9]+)$',views.DeleteEducation.as_view(), name='delete-education'),
    url(r'^add-employment$', views.AddEmployment.as_view(), name='employment'),
    url(r'^delete-employment/(?P<pk>[0-9]+)$',views.DeleteEmployment.as_view(), name='delete-employment'),
    url(r'^personal-details$', views.PersonalDetails.as_view(),name='personal-details'),
    url(r'^user-language-rate$', views.UserLanguageRating.as_view(),name='user-language-rate'),
    url(r'^set-location$', views.SetLocation.as_view(), name='set-location'),
    url(r'^set-hourly-rate$', views.SetHourlyRate.as_view(), name='set-hourly-rate'),
    url(r'^complete-profile$', views.CompleteProfile.as_view(),name='complete-profile'),
    url(r'^favourite-jobs$', views.FavouriteJob.as_view(), name='favourite-jobs'),
    url(r'^apply-job$', views.ApplyJob.as_view(), name='apply-job'),
    url(r'^matched-jobs-list$', views.MatchedJobList.as_view(),name='matched-jobs-list'),
    url(r'^favourite-jobs-list$',views.FavouriteJobList.as_view(), name='favourite-jobs-list'),
    url(r'^my-jobs$',views.MyJobs.as_view(), name='my-jobs'),
    url(r'^job-completed/(?P<pk>[0-9]+)$',views.JobCompleted.as_view(), name='job-completed'),
    url(r'^job-pending/(?P<pk>[0-9]+)$',views.JobPending.as_view(), name='job-pending'),
    url(r'^job-approved$',views.JobApproved.as_view(), name='job-approved'),
    url(r'^job-closed/(?P<pk>[0-9]+)$',views.JobClosed.as_view(), name='job-closed'),
    url(r'^job-declined/(?P<pk>[0-9]+)$',views.JobDeclined.as_view(), name='job-declined'),
    url(r'^notification$',views.Notification.as_view(), name='notification'),
    url(r'^seen-notification$',views.NotificationSeen.as_view(), name='seen-notification'),
    url(r'^read-notification/(?P<pk>[0-9]+)$',views.NotificationRead.as_view(), name='read-notification'),
    url(r'^job-approval/(?P<user>[0-9a-f-]+)/(?P<applied>[0-9a-f-]+)$',views.JobApproval.as_view(), name='job-approval'),
    url(r'^user-profile/(?P<user>[0-9a-f-]+)$',views.UserProfile.as_view(), name='user-profile'),
    ################ Rating Managment ###########
    url(r'^review-company/(?P<pk>[0-9]+)$', views.ReviewCompany.as_view(),name='review-company'),
    ############### Job Post Creation URL ###############
    url(r'^job-post-step-1$', views.JobPost.as_view(), name='job-post'),
    url(r'^edit-job-post-step-1/(?P<uuid>[0-9a-f-]+)$',views.EditJobPost.as_view(), name='edit-job-post'),
    url(r'^job-post-step-2/(?P<uuid>[0-9a-f-]+)$',views.JobPostStep2.as_view(), name='job-post-step-2'),
    url(r'^job-post-step-3/(?P<uuid>[0-9a-f-]+)$',views.JobPostStep3.as_view(), name='job-post-step-3'),
    url(r'^job-post-step-4/(?P<uuid>[0-9a-f-]+)$',views.JobPostStep4.as_view(), name='job-post-step-4'),

    ############### Company Profile Management URL ###############
    url(r'^view-jobseeker/(?P<uuid>[0-9a-f-]+)$',views.ViewJobSeeker.as_view(), name='view-jobseeker'),
    url(r'^view-applicants/(?P<uuid>[0-9a-f-]+)/$',views.ViewApplicants.as_view(), name='view-applicants'),
    url(r'^company-profile$', views.CompanyProfile.as_view(),name='company-profile'),
    ############### Static Moanagment URL #######################
    url(r'^about-us$', views.AboutUsView.as_view(), name='aboutus'),
    url(r'^contact-us$', views.ContactUs.as_view(), name='contactus'),
    url(r'^faq$', views.Faq.as_view(), name='faq'),
    url(r'^privacypolicy$', views.PrivacyPolicyView.as_view(), name='privacypolicy'),
    url(r'^career$', views.Career.as_view(), name='career'),
    url(r'^terms$', views.Terms.as_view(), name='terms'),

    ################# Posted Job View URL ##############
    url(r'^posted-job-view/(?P<uuid>[0-9a-f-]+)/$',views.ViewPostedJobs.as_view(), name='posted-job-view'),
    url(r'^job-detail/(?P<uuid>[0-9a-f-]+)/$',views.JobsDetail.as_view(), name='job-detail'),
    url(r'^posted-job-delete/(?P<uuid>[0-9a-f-]+)/$',views.DeletePostedJobs.as_view(), name='posted-job-delete'),

    ####################### Chat URL ##########################
    url(r'^message/(?P<company>[0-9a-f-]+)/(?P<jobseeker>[0-9a-f-]+)/(?P<job>[0-9a-f-]+)$',views.Message.as_view(), name='message'),
    url(r'^message$',views.MessageRedirect.as_view(), name='message-redirect'),
    url(r'^delete-chat-message$',views.DeleteChatMessage.as_view(), name='delete-chat-message'),
    url(r'^delete-chatlist$',views.DeleteChatList.as_view(), name='delete-chatlist'),
    url(r'^invitation-accept/(?P<pk>[0-9]+)$',views.InvitationAccept.as_view(), name='invitation-accept'),

    ################# Apply to this job contract URL #####
    # url(r'^contract$', views.Contract.as_view(), name='contract'),

    ################Global Search URL###########
    url(r'^search$', views.JobSeekerSearch.as_view(),name='search'),
    url(r'^company-search$', views.CompanySearch.as_view(),name='company-search'),
    ################View Applicants Dashboard URL###########
    url(r'^company-dashboard$', views.CompanyDashboard.as_view(),name='company-dashboard'),
    ################ Company Dashboard Filter URL###########
    url(r'^company-search-filter$', views.CompanyDashboardFilter.as_view(),name='company-search-filter'),
    ################ Payment managment###########
    url(r'^advance-payment$', views.AdvancePayment.as_view(),name='advance-payment'),
    url(r'^paypal-payment-advance/(?P<pk>[0-9]+)$', views.PaypalPaymentAdvance.as_view(),name='paypal-payment-escrow'),
    url(r'^paypal-payment-escrow/(?P<pk>[0-9]+)$', views.PaypalPaymentEscrow.as_view(),name='paypal-payment-escrow'),
    url(r'^release-payment/(?P<pk>[0-9]+)$', views.ReleasePayment.as_view(),name='paypal-payment-escrow'),
    ################ Top Skills Managment ###########
    url(r'^top-skills$', views.TopSkills.as_view(),name='top-skills'),
    url(r'^top-skills-action$', views.TopSkillsAction.as_view(),name='top-skills-action'),
    url(r'^refer-friend$', views.ReferFriendView.as_view(),name='refer-friend'),

]
