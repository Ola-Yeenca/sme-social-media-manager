#!/usr/bin/env python3
"""
SME Analytica Specific Content Generator
Creates authentic, valuable content based on real SME Analytica features and results
"""

import os
import sys
import asyncio
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Unset the shell environment variable to use .env file
if 'SOCIAL_MEDIA_DB_ID' in os.environ:
    del os.environ['SOCIAL_MEDIA_DB_ID']

class SMEAnalyticaContentGenerator:
    """Generate authentic SME Analytica content based on real features and results"""
    
    def __init__(self):
        # Real SME Analytica content themes
        self.content_themes = {
            "data_monday": {
                "english": [
                    "📊 Data Monday: MenuFlow users report ~10% higher margins during peak hours thanks to AI pricing. That's real money in your pocket! #SMEAnalytica #MenuFlow #DynamicPricing",
                    "📈 Monday Insight: Small restaurants using our QR + analytics serve more guests per hour with minimal wait time. Data = efficiency! #RestaurantTech #AIforSMEs",
                    "💡 Data Tip Monday: Track your foot-traffic patterns with a simple heatmap - reveals your goldmine hours for dynamic pricing #BusinessIntelligence #SMEGrowth"
                ],
                "spanish": [
                    "📊 Lunes de Datos: Usuarios de MenuFlow reportan ~10% más márgenes en horas pico gracias a precios IA. ¡Dinero real en tu bolsillo! #SMEAnalytica #MenuFlow",
                    "📈 Insight Lunes: Restaurantes pequeños usando nuestro QR + analíticas sirven más huéspedes por hora con espera mínima. ¡Datos = eficiencia! #RestaurantesTech",
                    "💡 Consejo Lunes: Rastrea patrones de tráfico peatonal con mapa de calor - revela tus horas doradas para precios dinámicos #InteligenciaNegocios"
                ]
            },
            "talk_tuesday": {
                "english": [
                    "💬 Talk Tuesday: Restaurant owners, what's your biggest challenge - pricing, inventory, or customer insights? We solve all three with MenuFlow! #TalkTuesday #RestaurantTech",
                    "🗣️ Tuesday Question: How do you currently decide when to raise prices during busy periods? Our AI does it automatically - 10% margin boost proven! #SMEAnalytica",
                    "🤔 Let's Talk: Which would boost your revenue most? Dynamic Pricing | Real-time Analytics | QR Ordering | AI Insights? We have them all! #BusinessGrowth"
                ],
                "spanish": [
                    "💬 Martes de Charla: Dueños de restaurantes, ¿cuál es su mayor desafío - precios, inventario o insights de clientes? ¡Resolvemos los tres con MenuFlow! #RestaurantesTech",
                    "🗣️ Pregunta Martes: ¿Cómo decides actualmente cuándo subir precios en períodos ocupados? Nuestra IA lo hace automáticamente - ¡10% más margen comprobado! #SMEAnalytica",
                    "🤔 Hablemos: ¿Qué aumentaría más tus ingresos? Precios Dinámicos | Analíticas Tiempo Real | Pedidos QR | Insights IA? ¡Tenemos todo! #CrecimientoNegocios"
                ]
            },
            "case_wednesday": {
                "english": [
                    "🏆 Case Wednesday: Local café saw 10% higher margins during weekend rush with MenuFlow's AI pricing. Real results, real profits! #CaseStudy #MenuFlow #Success",
                    "📈 Wednesday Win: Restaurant using our QR + analytics serves more guests per hour, minimal wait. Efficiency meets profitability! #SMEAnalytica #RestaurantTech",
                    "🎯 Case Study: Hotel manager uses our occupancy + feedback analytics for perfect RevPAR optimization. Data-driven hospitality! #HotelTech #BusinessIntelligence"
                ],
                "spanish": [
                    "🏆 Caso Miércoles: Café local vio 10% más márgenes durante rush de fin de semana con precios IA de MenuFlow. ¡Resultados reales, ganancias reales! #CasoEstudio #MenuFlow",
                    "📈 Victoria Miércoles: Restaurante usando nuestro QR + analíticas sirve más huéspedes por hora, espera mínima. ¡Eficiencia encuentra rentabilidad! #SMEAnalytica",
                    "🎯 Caso de Estudio: Gerente de hotel usa nuestras analíticas de ocupación + feedback para optimización RevPAR perfecta. ¡Hospitalidad basada en datos! #HotelTech"
                ]
            },
            "tech_thursday": {
                "english": [
                    "⚡ Tech Thursday: MenuFlow = QR ordering + AI pricing + real-time analytics = restaurant super-tool. All in one platform! #TechThursday #MenuFlow #RestaurantTech",
                    "🔧 Thursday Tech: We integrate into your existing POS/booking systems and turn them into super-tools. No vendor changes needed! #SMEAnalytica #Integration",
                    "💻 Tech Tip Thursday: Built so you don't need to be a data scientist to make smarter decisions. Enterprise analytics made simple! #AIforSMEs #BusinessIntelligence"
                ],
                "spanish": [
                    "⚡ Jueves Tech: MenuFlow = pedidos QR + precios IA + analíticas tiempo real = súper-herramienta restaurante. ¡Todo en una plataforma! #JuevesTech #MenuFlow",
                    "🔧 Jueves Tecnología: Nos integramos en tus sistemas POS/reservas existentes y los convertimos en súper-herramientas. ¡Sin cambios de proveedor! #SMEAnalytica",
                    "💻 Consejo Tech Jueves: Construido para que no necesites ser científico de datos para tomar decisiones más inteligentes. ¡Analíticas empresariales simplificadas! #IAparaPYMEs"
                ]
            },
            "fact_friday": {
                "english": [
                    "💡 Fact Friday: 63% of restaurateurs plan to invest in QR tech - we're already there with MenuFlow! Early adopters win big 🚀 #FactFriday #QRMenus #RestaurantTech",
                    "📊 Friday Fact: SME Analytica turns raw sales data into actionable insights without complex setup. No data scientist required! #SMEAnalytica #DataInsights",
                    "🎯 Fun Fact Friday: Our AI alerts retail shops when demand spikes (like beach gear in summer) - no more stockouts or guesswork! #RetailAnalytics #AIforSMEs"
                ],
                "spanish": [
                    "💡 Viernes de Datos: 63% de restauradores planean invertir en tecnología QR - ¡nosotros ya estamos ahí con MenuFlow! Los adoptadores tempranos ganan grande 🚀 #ViernesDatos",
                    "📊 Dato Viernes: SME Analytica convierte datos de ventas en insights accionables sin configuración compleja. ¡No se requiere científico de datos! #SMEAnalytica",
                    "🎯 Dato Curioso Viernes: Nuestra IA alerta tiendas cuando demanda aumenta (como equipo de playa en verano) - ¡no más desabastecimiento! #AnalíticasRetail #IAparaPYMEs"
                ]
            },
            "weekend_insights": {
                "english": [
                    "🌟 Weekend Insight: Bar owners using our nightlife analytics module raise cover charges on busy weekends automatically. Smart pricing = more profit! #WeekendVibes #NightlifeAnalytics",
                    "☀️ Saturday Success: Early MenuFlow adopters serve more guests per hour with minimal wait time using our AI suggestions. Weekend rush? No problem! #MenuFlow #RestaurantTech",
                    "🎉 Sunday Spotlight: SME Analytica's vertical-specific modules (restaurants, hotels, retail) include industry features out of the box. No generic solutions here! #SMEAnalytica #VerticalFocus"
                ],
                "spanish": [
                    "🌟 Insight Fin de Semana: Dueños de bares usando nuestro módulo de analíticas nocturnas suben precios de entrada en fines de semana ocupados automáticamente. ¡Precios inteligentes = más ganancia! #VibesFinDeSemana",
                    "☀️ Éxito Sábado: Adoptadores tempranos de MenuFlow sirven más huéspedes por hora con tiempo de espera mínimo usando nuestras sugerencias IA. ¿Rush de fin de semana? ¡No hay problema! #MenuFlow",
                    "🎉 Domingo Spotlight: Los módulos verticales específicos de SME Analytica (restaurantes, hoteles, retail) incluyen características de industria listas. ¡No hay soluciones genéricas aquí! #SMEAnalytica"
                ]
            }
        }
        
        # Engagement posts for community building
        self.engagement_posts = {
            "english": [
                "🤔 SME owners: What's your biggest data challenge? Understanding customer patterns, optimizing pricing, or tracking performance? Let's solve it together! #SMEAnalytica #BusinessIntelligence",
                "🗳️ POLL: Which MenuFlow feature excites you most? QR Ordering | AI Pricing | Real-time Analytics | Customer Insights #MenuFlow #RestaurantTech",
                "💬 Question: How much time do you spend manually analyzing sales data each week? Our AI does it in seconds! #DataAutomation #SMEGrowth",
                "🎯 Share: Tell us about a time when better data could have saved you money or boosted profits! #BusinessStories #DataDriven",
                "🤝 Tag a fellow restaurant/hotel/retail owner who needs to see MenuFlow's 10% margin boost results! #SMEAnalytica #BusinessGrowth"
            ],
            "spanish": [
                "🤔 Dueños PYME: ¿Cuál es su mayor desafío de datos? ¿Entender patrones de clientes, optimizar precios o rastrear rendimiento? ¡Resolvámoslo juntos! #SMEAnalytica #InteligenciaNegocios",
                "🗳️ ENCUESTA: ¿Qué característica de MenuFlow te emociona más? Pedidos QR | Precios IA | Analíticas Tiempo Real | Insights Clientes #MenuFlow #RestaurantesTech",
                "💬 Pregunta: ¿Cuánto tiempo gastas analizando manualmente datos de ventas cada semana? ¡Nuestra IA lo hace en segundos! #AutomatizaciónDatos #CrecimientoPYME",
                "🎯 Comparte: ¡Cuéntanos sobre una vez cuando mejores datos podrían haberte ahorrado dinero o aumentado ganancias! #HistoriasNegocios #BasadoEnDatos",
                "🤝 Etiqueta a un compañero dueño de restaurante/hotel/retail que necesita ver los resultados de 10% más margen de MenuFlow! #SMEAnalytica #CrecimientoNegocios"
            ]
        }
        
        # Feature highlights showcasing real SME Analytica capabilities
        self.feature_highlights = {
            "english": [
                "⚡ SME MAGIC: We integrate into your existing POS/booking systems and turn them into super-tools. No vendor changes, just enhanced capabilities! #SMEAnalytica #Integration #BusinessIntelligence",
                "🚀 MENUFLOW POWER: QR ordering + AI pricing + real-time analytics = complete restaurant solution. Early users report 10% margin boost! #MenuFlow #RestaurantTech #DynamicPricing",
                "💡 NO TECH NEEDED: Built so you don't need to be a data scientist to make smarter decisions. Enterprise analytics made simple for SMEs! #AIforSMEs #UserFriendly #BusinessIntelligence",
                "🎯 VERTICAL FOCUS: Dedicated modules for restaurants (MenuFlow), hotels, retail - industry-specific features out of the box, not generic solutions! #SMEAnalytica #VerticalSpecialization #IndustryFocus",
                "📊 REAL-TIME INSIGHTS: Track live customer traffic, table turns, kitchen flow - instant insights for immediate action. Data when you need it! #RealTimeAnalytics #OperationalIntelligence #SMEAnalytica"
            ],
            "spanish": [
                "⚡ MAGIA SME: Nos integramos en tus sistemas POS/reservas existentes y los convertimos en súper-herramientas. ¡Sin cambios de proveedor, solo capacidades mejoradas! #SMEAnalytica #Integración",
                "🚀 PODER MENUFLOW: Pedidos QR + precios IA + analíticas tiempo real = solución completa restaurante. ¡Usuarios tempranos reportan 10% más margen! #MenuFlow #RestaurantesTech",
                "💡 NO SE NECESITA TECH: Construido para que no necesites ser científico de datos para tomar decisiones más inteligentes. ¡Analíticas empresariales simplificadas para PYMEs! #IAparaPYMEs",
                "🎯 ENFOQUE VERTICAL: Módulos dedicados para restaurantes (MenuFlow), hoteles, retail - características específicas de industria listas, ¡no soluciones genéricas! #SMEAnalytica #EspecializaciónVertical",
                "📊 INSIGHTS TIEMPO REAL: Rastrea tráfico de clientes en vivo, rotación de mesas, flujo de cocina - insights instantáneos para acción inmediata. ¡Datos cuando los necesitas! #AnalíticasTiempoReal #SMEAnalytica"
            ]
        }

    def get_daily_theme_content(self, day_of_week, language="auto"):
        """Get content for specific day theme"""
        
        themes = {
            0: "data_monday",
            1: "talk_tuesday", 
            2: "case_wednesday",
            3: "tech_thursday",
            4: "fact_friday",
            5: "weekend_insights",
            6: "weekend_insights"
        }
        
        theme = themes.get(day_of_week, "data_monday")
        
        # Auto language selection (70% English, 30% Spanish)
        if language == "auto":
            language = "spanish" if random.random() < 0.3 else "english"
        
        content_options = self.content_themes[theme][language]
        return random.choice(content_options)

    def get_engagement_content(self, language="auto"):
        """Get engagement/community building content"""
        
        if language == "auto":
            language = "spanish" if random.random() < 0.3 else "english"
        
        return random.choice(self.engagement_posts[language])

    def get_feature_highlight(self, language="auto"):
        """Get feature highlight content"""
        
        if language == "auto":
            language = "spanish" if random.random() < 0.3 else "english"
        
        return random.choice(self.feature_highlights[language])

    def generate_daily_content_plan(self):
        """Generate a full day's content plan with SME Analytica focus"""
        
        today = datetime.now()
        day_of_week = today.weekday()
        
        # Content distribution for the day
        content_plan = []
        
        # Optimal posting times
        posting_times = [
            {"hour": 8, "minute": 0, "type": "theme"},      # Morning theme content
            {"hour": 10, "minute": 30, "type": "engagement"}, # Mid-morning engagement
            {"hour": 12, "minute": 0, "type": "feature"},    # Lunch feature highlight
            {"hour": 15, "minute": 0, "type": "theme"},      # Afternoon theme content
            {"hour": 17, "minute": 30, "type": "engagement"}, # End-of-day engagement
            {"hour": 19, "minute": 0, "type": "feature"}     # Evening feature highlight
        ]
        
        for i, time_slot in enumerate(posting_times):
            # Generate content based on type
            if time_slot["type"] == "theme":
                content = self.get_daily_theme_content(day_of_week)
                category = "educational"
            elif time_slot["type"] == "engagement":
                content = self.get_engagement_content()
                category = "community"
            else:  # feature
                content = self.get_feature_highlight()
                category = "promotional"
            
            # Calculate scheduled time
            scheduled_time = today.replace(
                hour=time_slot["hour"],
                minute=time_slot["minute"],
                second=0,
                microsecond=0
            )
            
            # If time has passed, schedule for tomorrow
            if scheduled_time <= datetime.now():
                scheduled_time += timedelta(days=1)
            
            # Extract hashtags from content
            hashtags = []
            if "#" in content:
                words = content.split()
                hashtags = [word for word in words if word.startswith("#")]
                # Remove hashtags from content for cleaner storage
                content_clean = " ".join([word for word in words if not word.startswith("#")])
            else:
                content_clean = content
                hashtags = ["#SMEAnalytica", "#MenuFlow", "#AIforSMEs"]
            
            content_plan.append({
                "content": content_clean,
                "hashtags": hashtags[:8],  # Limit to 8 hashtags
                "scheduled_time": scheduled_time,
                "category": category,
                "content_type": time_slot["type"],
                "post_number": i + 1
            })
        
        return content_plan


async def generate_sme_analytica_content():
    """Generate SME Analytica specific content for the day"""
    
    print("🚀 SME Analytica Content Generation")
    print("=" * 60)
    print("Creating authentic, valuable content based on real features and results")
    
    try:
        from notion import NotionManager, SocialMediaPost, PostStatus, Platform, PostType
        
        # Initialize components
        notion_manager = NotionManager()
        content_generator = SMEAnalyticaContentGenerator()
        
        print("✅ Components initialized")
        
        # Generate daily content plan
        content_plan = content_generator.generate_daily_content_plan()
        
        print(f"\n📋 Generating {len(content_plan)} SME Analytica posts...")
        
        created_posts = []
        
        for plan in content_plan:
            print(f"\n{plan['post_number']}. Creating {plan['category']} post...")
            print(f"   Type: {plan['content_type']}")
            print(f"   Time: {plan['scheduled_time'].strftime('%H:%M')}")
            print(f"   Content: {plan['content'][:60]}...")
            
            # Create post
            post = SocialMediaPost(
                name=f"SME Analytica - {plan['category'].title()} {datetime.now().strftime('%Y-%m-%d')} #{plan['post_number']}",
                content=plan['content'],
                status=PostStatus.SCHEDULED,
                platform=Platform.TWITTER,
                post_type=PostType.INFORMATIONAL,
                scheduled_time=plan['scheduled_time'],
                language="Auto (70% EN, 30% ES)",
                content_theme=plan['category'],
                ai_provider_used="SME Analytica Content Generator",
                tags=plan['hashtags']
            )
            
            # Save to Notion
            post_id = notion_manager.create_post(post)
            
            if post_id:
                print(f"   ✅ Created successfully")
                created_posts.append({
                    "id": post_id,
                    "category": plan['category'],
                    "time": plan['scheduled_time']
                })
            else:
                print(f"   ❌ Failed to create post")
        
        # Summary
        print(f"\n" + "=" * 60)
        print(f"🎉 SME Analytica Content Generation Complete!")
        print(f"📊 Created: {len(created_posts)} authentic posts")
        print(f"📅 Scheduled over: {len(set(p['time'].hour for p in created_posts))} time slots")
        
        # Show breakdown by category
        categories = {}
        for post in created_posts:
            cat = post['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"\n📋 Content Breakdown:")
        for category, count in categories.items():
            print(f"   • {category.title()}: {count} posts")
        
        print(f"\n🎯 Content Features:")
        print(f"   • Real SME Analytica features and results")
        print(f"   • Bilingual strategy (70% English, 30% Spanish)")
        print(f"   • Daily themes (Data Monday, Tech Thursday, etc.)")
        print(f"   • Authentic case studies and success stories")
        print(f"   • Community engagement and value-driven content")
        
        return len(created_posts)
        
    except Exception as e:
        print(f"❌ Error generating SME Analytica content: {e}")
        import traceback
        traceback.print_exc()
        return 0


if __name__ == "__main__":
    asyncio.run(generate_sme_analytica_content())
