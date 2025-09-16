"""
Paquete de esquemas Pydantic para la aplicación Visart
Exporta todos los esquemas para fácil acceso
"""

# Importar esquemas de usuario
from .user_schemas import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserPublicResponse,
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserLogin,
    Token,
    TokenData,
    UserPasswordUpdate,
    FollowCreate,
    FollowResponse,
    UserStatsResponse,
    UserListResponse,
    FollowListResponse,
    UserSearchFilters,
    UserAdminResponse,
    UserAdminUpdate,
    UserNotificationSettings
)

# Importar esquemas de publicaciones
from .post import (
    PostBase,
    PostCreate,
    PostUpdate,
    PostResponse,
    PostDetailResponse,
    PostListResponse,
    PostOwnerResponse,
    LikeCreate,
    LikeResponse,
    CommentBase,
    CommentCreate,
    CommentResponse,
    CommentUpdate,
    CommentOwnerResponse,
    PostSearchFilters,
    PostStatsResponse,
    FeedFilters
)

# Exportar todos los esquemas
__all__ = [
    # User schemas
    'UserBase',
    'UserCreate',
    'UserUpdate',
    'UserResponse',
    'UserPublicResponse',
    'UserProfileCreate',
    'UserProfileUpdate',
    'UserProfileResponse',
    'UserLogin',
    'Token',
    'TokenData',
    'UserPasswordUpdate',
    'FollowCreate',
    'FollowResponse',
    'UserStatsResponse',
    'UserListResponse',
    'FollowListResponse',
    'UserSearchFilters',
    'UserAdminResponse',
    'UserAdminUpdate',
    'UserNotificationSettings',
    
    # Post schemas
    'PostBase',
    'PostCreate',
    'PostUpdate',
    'PostResponse',
    'PostDetailResponse',
    'PostListResponse',
    'PostOwnerResponse',
    'LikeCreate',
    'LikeResponse',
    'CommentBase',
    'CommentCreate',
    'CommentResponse',
    'CommentUpdate',
    'CommentOwnerResponse',
    'PostSearchFilters',
    'PostStatsResponse',
    'FeedFilters'
]
