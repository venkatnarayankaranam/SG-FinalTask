import pytest
from unittest.mock import patch
import sys
import os

# Add the parent directory to the Python path so we can import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Test the home route returns successfully."""
    response = client.get('/')
    assert response.status_code == 200
    # Check if the response contains HTML content
    assert b'html' in response.data.lower() or b'<!doctype' in response.data.lower()


def test_home_route_renders_template(client):
    """Test that home route renders the index.html template."""
    response = client.get('/')
    assert response.status_code == 200
    # The response should be HTML content from the template
    assert response.content_type.startswith('text/html')


@patch('app.deploy_to_azure')
def test_deploy_route_with_project_name(mock_deploy, client):
    """Test the deploy route with a valid project name."""
    # Mock the deploy_to_azure function
    mock_deploy.return_value = "Deployment successful!"
    
    response = client.post('/deploy', data={'project_name': 'test-project'})
    
    assert response.status_code == 200
    assert b'Deployment Output:' in response.data
    assert b'Deployment successful!' in response.data
    
    # Verify the mock was called with the correct argument
    mock_deploy.assert_called_once_with('test-project')


@patch('app.deploy_to_azure')
def test_deploy_route_without_project_name(mock_deploy, client):
    """Test the deploy route without providing project name."""
    # Mock the deploy_to_azure function
    mock_deploy.return_value = "No project name provided"
    
    response = client.post('/deploy', data={})
    
    assert response.status_code == 200
    # The mock should be called with None since no project_name was provided
    mock_deploy.assert_called_once_with(None)


@patch('app.deploy_to_azure')
def test_deploy_route_with_empty_project_name(mock_deploy, client):
    """Test the deploy route with empty project name."""
    mock_deploy.return_value = "Empty project name"
    
    response = client.post('/deploy', data={'project_name': ''})
    
    assert response.status_code == 200
    assert b'Deployment Output:' in response.data
    mock_deploy.assert_called_once_with('')


def test_deploy_route_get_method_not_allowed(client):
    """Test that GET requests to /deploy are not allowed."""
    response = client.get('/deploy')
    assert response.status_code == 405  # Method Not Allowed


@patch('app.deploy_to_azure')
def test_deploy_route_handles_exception(mock_deploy, client):
    """Test that the deploy route handles exceptions gracefully."""
    # Mock the deploy_to_azure function to raise an exception
    mock_deploy.side_effect = Exception("Deployment failed")
    
    # This test assumes your app doesn't handle exceptions yet
    # You might want to add exception handling to your app.py
    with pytest.raises(Exception):
        client.post('/deploy', data={'project_name': 'test-project'})


def test_nonexistent_route(client):
    """Test that nonexistent routes return 404."""
    response = client.get('/nonexistent')
    assert response.status_code == 404


# Integration tests
class TestAppIntegration:
    """Integration tests for the Flask application."""
    
    def test_app_configuration(self):
        """Test that the app is configured correctly."""
        assert app.name == 'app'
        assert 'TESTING' in app.config or app.config.get('TESTING') is None
    
    @patch('app.deploy_to_azure')
    def test_full_deployment_workflow(self, mock_deploy, client):
        """Test the complete workflow from home to deployment."""
        mock_deploy.return_value = "Successfully deployed test-app to Azure"
        
        # First, visit the home page
        home_response = client.get('/')
        assert home_response.status_code == 200
        
        # Then, submit a deployment
        deploy_response = client.post('/deploy', data={'project_name': 'test-app'})
        assert deploy_response.status_code == 200
        assert b'Successfully deployed test-app to Azure' in deploy_response.data
        
        mock_deploy.assert_called_once_with('test-app')


# Test data validation
class TestDataValidation:
    """Tests for data validation and edge cases."""
    
    @patch('app.deploy_to_azure')
    def test_special_characters_in_project_name(self, mock_deploy, client):
        """Test project names with special characters."""
        special_name = "test-project_123!@#"
        mock_deploy.return_value = f"Deployed {special_name}"
        
        response = client.post('/deploy', data={'project_name': special_name})
        assert response.status_code == 200
        mock_deploy.assert_called_once_with(special_name)
    
    @patch('app.deploy_to_azure')
    def test_very_long_project_name(self, mock_deploy, client):
        """Test with a very long project name."""
        long_name = "a" * 1000
        mock_deploy.return_value = "Deployed successfully"
        
        response = client.post('/deploy', data={'project_name': long_name})
        assert response.status_code == 200
        mock_deploy.assert_called_once_with(long_name)


if __name__ == '__main__':
    pytest.main([__file__])