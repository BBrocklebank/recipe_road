import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
if os.path.exists('env.py'):
    import env

