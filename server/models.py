from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name', 'phone_number')
    def validate_author_details(self, key, value):
        if key == "name":
            if not value:
                raise ValueError('Please enter a name')
            author = Author.query.filter(Author.name == value).first()
            if author:
                raise ValueError('name must be unique')
            return value
        if key == "phone_number":
            if len(value) != 10 or not value.isdigit():
                raise ValueError('Please enter a valid phone number')
            return value
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content', 'summary', 'category', 'title')
    def validate_post_details(self, key, value):
        if key == 'content':
            if len(value) < 250:
                raise ValueError('content must be at least 250 characters')
            return value
        if key == 'summary':
            if len(value) > 250:
                raise ValueError("Post summary must be less than or equal to 250 characters long.")
            return value
        if key == 'category':
            if value != 'Fiction' and value != 'Non-Fiction':
                raise ValueError("Category must be Fiction or Non-Fiction.")
            return value
        if key == 'title':
            if not value:
                raise ValueError("Title field is required.")
            clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
            if not any(substring in value for substring in clickbait):
                raise ValueError("No clickbait found")
            return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
