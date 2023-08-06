from troj_session import TrojSession
# from dotenv import load_dotenv
import troj_dataset
import troj_client

# load_dotenv()


def start(api_key=None, token=None, app_id=None, app_key=None):
    '''
    This is the troj package's main function
    Initializes all the classes and saves them under the session superclass for use later

    '''
    # Instantiate session super class
    user_session = TrojSession()
    # instantiate client to make and recieve requests
    client = troj_client.TrojClient()
    # instantiate dataset to create a dataframe in the future
    ds = troj_dataset.TrojDataset()
    # use client function to set all credentials
    client.set_credentials(api_key=api_key, token=token,
                           app_id=app_id, app_key=app_key)
    # associate the subclasses with the session superclass
    user_session.dataset = ds
    user_session.client = client
    # return session superclass
    return user_session
