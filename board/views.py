import json

from django.views import View
from django.http  import JsonResponse
from json.decoder import JSONDecodeError

from board.models     import Board
from users.decorator  import SignIn_decorator

class PostView(View):
    @SignIn_decorator
    def post(self, request):
        try :
            data    = json.loads(request.body)
            user    = request.user
            title   = data['title'] 
            content = data['content']
    
            Board.objects.create(
                user    = user,
                title   = title,
                content = content,         
            )
        
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except JSONDecodeError :
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
    
    def get(self, request):
        offset = int(request.GET.get("offset",0))
        limit  = int(request.GET.get("limit",100))
        sort   = request.GET.get('sort')   
        
        limit     = offset + limit
        sort_by   = {
            'recent' : '-created_at',
            'old'    : 'created_at'
        }
        
        boards  = Board.objects.select_related('user').all().order_by(sort_by.get(sort, '-created_at'))[offset : limit]

        board_list = [{
            'board_id'    : board.id,
            'author'      : board.user.name,
            'title'       : board.title,
            'content'     : board.content,
            'created_at'  : board.created_at
        } for board in boards]

        return JsonResponse({'board_list' : board_list}, status=200)

class PostDetailView(View):
    def get(self, request, board_id):
        try:
            if not Board.objects.filter(id = board_id).exists():
                return JsonResponse({'message' : 'BOARD_DOES_NOT_EXIST'}, status=404)
        
            board = Board.objects.select_related('user').get(id = board_id)     

            board_info = {
                'board_id'   : board.id,
                'author'     : board.user.name,
                'title'      : board.title,
                'content'    : board.content,
                'created_at' : board.created_at.strftime("%Y/%m/%d %H:%M")
            }
        
            return JsonResponse({'board_info': board_info,} ,status=200)
        
        except Board.DoesNotExist:
            return JsonResponse({'message' : 'BOARD_DOES_NOT_EXIST'}, status=404)
        
        except Board.MultipleObjectsReturned:
            return JsonResponse({'message' : 'BOARD_MULTIPE_ERROR'}, status = 400)

    @SignIn_decorator
    def delete(self, request, board_id):
        try:
            user = request.user
            if not Board.objects.filter(id = board_id).exists():
                return JsonResponse({'message' : 'BOARD_DOES_NOT_EXIST'}, status=404)
        
            board = Board.objects.get(id = board_id)
        
            if user != board.user:
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)
        
            board.delete()
            
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except Board.DoesNotExist:
            return JsonResponse({'message' : 'BOARD_DOES_NOT_EXIST'}, status=404)
        
        except Board.MultipleObjectsReturned:
            return JsonResponse({'message' : 'BOARD_MULTIPE_ERROR'}, status = 400)
        
    @SignIn_decorator
    def patch(self, request, board_id) :
        try: 
            user = request.user
            data = json.loads(request.body)

            if not Board.objects.filter(id=board_id).exists():
                return JsonResponse({'message' : 'BOARD_DOES_NOT_EXIST'}, status=404)
            
            board = Board.objects.get(id=board_id)
            
            if user != board.user :
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            
            board.title  = data.get('title', board.title)
            board.content = data.get('content', board.content)
            board.save()

            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except JSONDecodeError :
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except Board.DoesNotExist:
            return JsonResponse({'message' : 'BOARD_DOES_NOT_EXIST'}, status=404)
        
        except Board.MultipleObjectsReturned:
            return JsonResponse({'message' : 'BOARD_MULTIPE_ERROR'}, status = 400)