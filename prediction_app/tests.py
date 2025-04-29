# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.http import HttpResponse
# import json

# class HomeViewTest(TestCase):
    
#     def setUp(self):
#         """
#         Setting up the test user and data.
#         """
#         # You can set up any data that is necessary for your tests here
#         self.user = User.objects.create_user(username='testuser', password='password123')

#     def test_home_get(self):
#         """
#         Test that a GET request to the home view returns status 200 and the correct template is used.
#         """
#         response = self.client.get(reverse('home'))  # Assuming 'home' is your URL name
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'prediction_app/home.html')

#     def test_home_post_valid_data(self):
#         """
#         Test that a POST request with valid data triggers prediction and chart generation.
#         """
#         data = {
#             'investment_amount': 1000000,
#             'number_of_investors': 5,
#             'year_founded': 2015,
#             'industry': 'Tech',
#             'country': 'USA'
#         }
#         response = self.client.post(reverse('home'), data)

#         # Print the content of the response to help debug
#         print(response.content)  # Debugging line

#         # Check if the response contains the expected prediction and chart div
#         self.assertContains(response, 'Predicted Growth Rate')
#         self.assertContains(response, 'chart_div')  # You can check for presence of chart here
#         self.assertNotContains(response, 'Error')  # Ensure no errors are returned
        
        
#         # response = self.client.post(reverse('home'), post_data)
#         # self.assertEqual(response.status_code, 200)
        
#         # # Ensure prediction value is in the response
#         # self.assertContains(response, 'Predicted Growth Rate')

#         # # Check if chart_div exists (i.e., chart is being rendered)
#         # self.assertIn('chart_div', response.context)

#         # # Check for comparison_chart and scatter_chart in response context
#         # self.assertIn('comparison_chart', response.context)
#         # self.assertIn('scatter_chart', response.context)

#         # # Ensure the 'similar_info' is populated in the context
#         # self.assertIn('similar_info', response.context)

#     def test_home_post_invalid_data(self):
#         """
#         Test that a POST request with invalid data triggers an error message.
#         """
#         post_data = {
#             'investment_amount': 'invalid',  # Invalid value
#             'number_of_investors': 'ten',   # Invalid value
#             'year_founded': '2015',
#             'industry': 'Technology',
#             'country': 'USA'
#         }
#         response = self.client.post(reverse('home'), post_data)
#         self.assertEqual(response.status_code, 200)

#         # Check if the error message is in the response
#         self.assertIn('Error:', response.context['error'])

#     def test_home_post_missing_data(self):
#         """
#         Test that a POST request with missing data triggers an error message.
#         """
#         post_data = {
#             'investment_amount': '1000000',
#             'number_of_investors': 5,
#             # 'year_founded' is missing
#             'industry': 'Technology',
#             'country': 'USA'
#         }
#         response = self.client.post(reverse('home'), post_data)
#         self.assertEqual(response.status_code, 200)

#         # Ensure error message is displayed for missing field
#         self.assertIn('Error:', response.context['error'])

#     def test_home_get_no_data(self):
#         """
#         Test that a GET request (without form data) returns a 200 response.
#         """
#         response = self.client.get(reverse('home'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Startup Growth Prediction')

#     def test_home_post_missing_feature_in_model(self):
#         """
#         Test for missing features in model during prediction (e.g., industry or country).
#         """
#         post_data = {
#             'investment_amount': '500000',
#             'number_of_investors': 10,
#             'year_founded': 2015,
#             'industry': 'NonExistingIndustry',  # Industry that doesn't exist in the model
#             'country': 'NonExistingCountry'     # Country that doesn't exist in the model
#         }
#         response = self.client.post(reverse('home'), post_data)
#         self.assertEqual(response.status_code, 200)
        
#         # Check that the error message is shown
#         self.assertIn('Error:', response.context['error'])

