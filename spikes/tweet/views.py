from django.shortcuts import render, redirect, get_object_or_404
from django.http import request
# Local Modules
from .models import Tweet  # DB
from .forms import TweetForms, UserRegistrationForm  # Forms Layout
from django.contrib.auth.decorators import login_required  # auth Decorator
from django.contrib.auth import login


def index(request):
    return render(request, 'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})


@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForms(request.POST, request.FILES)
        if form.is_valid():  # Checking Form is Valid or not
            tweet = form.save(commit=False)  # Save or Not | Commit is
            tweet.user = request.user  # Get Current User Logged and Tweet
            tweet.save()  # Save in DB
            return redirect('tweet_list')  # Redirect to tweet_list
    else:
        form = TweetForms()
    return render(request, 'tweet_form.html', {'form': form})


@login_required
def show_me(request, tweet_id):
    print(tweet_id)
    print(type(tweet_id))
    return render(request, 'index.html')


@login_required
def tweet_edit(request, tweet_id):
    print('Function Loading')
    try:
        # print(type(tweet_id))
        # Check if the tweet exists and belongs to the user
        print(tweet_id)
        print(request.user)
        tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
        print(f"Found tweet: {tweet}")

        if request.method == 'POST':
            form = TweetForms(request.POST, request.FILES, instance=tweet)
            print(f"Form is {form}")

            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                return redirect('tweet_list')
            else:
                print("Form is not valid")
        else:
            form = TweetForms(instance=tweet)

        print("Not A Post But its Get")
        return render(request, 'tweet_form.html', {'form': form})
    except Exception as Err:
        print(Err)
        return render(request, 'index.html')


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')

    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


def register(request):
    pass
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect(tweet_list)

    else:
        pass
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
