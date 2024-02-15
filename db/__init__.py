from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .models import Brand
from .models import Product
from .models import Review
from .models import ReviewTopicAssociation
from .models import Category
from .models import Topic
from .models import ProductCategoryAssociation
